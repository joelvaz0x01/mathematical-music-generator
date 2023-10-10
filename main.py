from fibonacci_music import *
from math import sqrt

if __name__ == '__main__':
    # diatonic scales
    diatonic_scales = {
        0: [2, 2, 1, 2, 2, 2, 1],  # ionico
        1: [2, 1, 2, 2, 2, 1, 2],  # dorico
        2: [1, 2, 2, 2, 1, 2, 2],  # frigio
        3: [2, 2, 2, 1, 2, 2, 1],  # lidio
        4: [2, 2, 1, 2, 2, 1, 2],  # misolidio
        5: [2, 1, 2, 2, 1, 2, 2],  # eolico
        6: [1, 2, 2, 1, 2, 2, 2]  # locrio
    }

    # chords positions/patterns and triad inversion
    chords_and_inversion = {
        # major chords
        0: {
            0: [0, 4, 3],  # root position
            1: [4, 3, 5],  # 1st inversion
            2: [7, 5, 4]  # 2nd inversion
        },
        # minor chords
        1: {
            0: [0, 3, 4],  # root position
            1: [3, 4, 5],  # 1st inversion
            2: [7, 5, 3]  # 2nd inversion
        },
        # diminished chord
        2: {
            0: [0, 3, 3],  # root position
            1: [3, 3, 6],  # 1st inversion
            2: [6, 6, 3]  # 2nd inversion
        },
        # augmented chord
        3: {
            0: [0, 4, 4],  # root position
            1: [4, 4, 4],  # 1st inversion
            2: [8, 4, 4]  # 2nd inversion
        }
    }

    # chords left hand (piano)
    l_piano_chords = {}

    # important information
    current_octave = 4
    filename_midi = 'fibonacci.mid'

    # useful array
    all_tracks = []

    # chromatic Scale
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # define beats per minute
    while True:
        try:
            beats_per_minute = int(input('Beats per minute to use (BPM): '))
            break
        except ValueError:
            print('\nInsert a valid number!')

    # get time signature, notes per bar and the sequences timers
    time_signature, notes_per_bar, sequence_timers = make_time_signature()

    # get the diatonic mode to use on midi project
    diatonic_mode = diatonic_selection(diatonic_scales, '', None)

    # select scale to use the previous diatonic mode
    while True:
        try:
            print('\nScales available: ', chromatic_scale)
            scale_to_use = input('Scale to use: ').upper()
            index_scale_note = chromatic_scale.index(scale_to_use)  # receive index number from `all_notes` array
            break
        except ValueError:
            print('Invalid note!')

    # get all notes on right hand (piano)
    r_piano = make_diatonic_scale([], index_scale_note, current_octave, diatonic_mode, chromatic_scale)

    # get all notes on left hand (piano)
    current_octave -= 2
    l_piano = make_diatonic_scale([], index_scale_note, current_octave, diatonic_mode, chromatic_scale)

    # calculate chords for all notes available on left hand (piano)
    l_piano_chords, inversion_used = chord_type({}, l_piano, chords_and_inversion, False, False, chromatic_scale)

    # show some useful information to the user
    print(f'\nScales in use:')
    print(f'\t{scale_to_use} scale (Octave {current_octave}):', r_piano)
    print(f'\t{scale_to_use} scale (Octave {current_octave}):', l_piano)
    print('\n{scale_to_use} scale chords That will be used on left hand:')
    for chords in l_piano_chords:
        print(f'\t{chords}:', l_piano_chords[chords])

    # build some calculations [`fibonacci_sequence`, `golden_ratio`]
    fib, golden_ratio = fibonacci_builder('', None), {0: str((1 + sqrt(5)) / 2)}

    # determine the pitches notes based on fibonacci sequence and golden ratio
    notes_pitches = make_pitches([], [], [fib, golden_ratio], [r_piano, l_piano], l_piano_chords, inversion_used,
                                 notes_per_bar, sequence_timers)

    # create midi tracks
    print('Creating stream. Please wait...')
    for notes_pitch in notes_pitches:
        all_tracks.append(create_track(beats_per_minute, time_signature, notes_pitch))

    # create score to put all midi tracks together
    score = music21.stream.Score()
    for track in all_tracks:
        score.insert(track)

    # convert music21.stream to midi format
    print('Converting stream to MIDI format. Please wait...')
    final_midi = music21.midi.translate.streamToMidiFile(score)

    # write the produced midi format
    print('Creating file', filename_midi)
    create_file(final_midi, filename_midi)
