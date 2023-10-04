import random
import music21
from math import sqrt, log2


def fibonacci(num, count, hashList, result):
    """ Calculate Fibonacci sequence.

    Parameters:
    num : INT maximum number to calculate the Fibonacci sequence.
    count : INT auxiliary variable that helps to build the Fibonacci sequence.
    hashList : DICTIONARY result of Fibonacci sequence (hash table).
    result : DICTIONARY result of Fibonacci sequence (hash table).

    Return type:
    DICTIONARY that contains the first 'num' numbers of Fibonacci sequence.

    Description:
    Calculate the first 'num' numbers of Fibonacci sequence using functional programing.
    """
    if num == count + 2:
        result = hashList
    else:
        tmp_res = int(hashList[count]) + int(hashList[count + 1])
        hashList.update({count + 2: str(tmp_res)})
        result = fibonacci(num, count + 1, hashList, result)
    return result


def diatonic_selection(diatonic_scale, error, result):
    """ Diatonic scales selection.

    Parameters:
    diatonic_scale : DICTIONARY all diatonic scales (hash table).
    error : STRING error string.
    result : LIST selected diatonic mode.

    Return type:
    LIST of position/pattern of the selected diatonic mode.

    Description:
    Select a diatonic scale to use as base.
    """
    if error:
        print(error)
    try:
        mode = int(
            input('Diatonic scale to use: \n1) Ionico\n2) Dorico\n3) Frigio\n4) Lidio\n5) Misolidio\n6) Eolico\n7) Locrio\nOption: '))
        if 1 <= mode <= 7:
            result = list(diatonic_scale.values())[mode - 1]
        else:
            result = diatonic_selection(diatonic_scale, 'Invalid mode!', result)
    except ValueError:
        result = diatonic_selection(diatonic_scale, 'Insert a valid number!', result)
    return result


def make_time_signature():
    """ Make time signature.

    Return type:
    LIST of the final time signature, the maximum notes in bars and the sequences timers.

    Description: Make and verify if is valid the time signature, notes per bar and the default Fibonacci and Golden Ratio sequences timers.
    """
    while True:
        time_sig = str(input('\nTime signature to use: ')).split('/')
        try:
            if len(time_sig) == 2:
                notes_bar = int(time_sig[0])
                note_type = int(time_sig[1])
                if not log2(note_type).is_integer() or note_type > 64 or notes_bar < 1 or note_type < 1:
                    raise ValueError
                break
            else:
                raise ValueError
        except ValueError:
            print('\nInvalid time signature!')
    fibonacci_note_time = 8 * (1 / 2) ** (log2(note_type) + 1)
    golden_ratio_note_time = notes_bar * fibonacci_note_time
    time_sig = f'{notes_bar}/{note_type}'
    print(f'\nTime signature that will be used:', time_sig, '\n')
    return time_sig, notes_bar, [fibonacci_note_time, golden_ratio_note_time]


def chord_type(result, note_to_scale, chords_list, scale_type_error, scale_position_error, all_notes):
    """ Make chords or triad inversions.

    Parameters:
    result : LIST result notes in chord (three notes).
    note_to_scale : LIST all notes to make a chord or a triad inversion.
    chords_list : LIST all chords positions/patterns or triad inversions.
    scale_type_error : BOOLEAN scale type error.
    scale_position_error : BOOLEAN scale position/pattern error.
    all_notes : LIST all chromatic scale.

    Return type:
    LIST of notes in chord and the chord position/pattern or triad inversion used.

    Description:
    Make chords or triad inversion with a given list of notes.
    """
    scale_type, scale_position = 0, 0
    while True:
        try:
            # Handle scale position
            if not scale_position_error:
                scale_type_error = True  # Need to be firstly True for try...exception work
                scale_type = int(input('\nScale type to use: \n1) Major chords\n2) Minor chords\n3) Diminished chord\n4) Augmented chord\nOption: '))
                if 1 <= scale_type <= 4:
                    scale_type_error = False
                else:
                    print('Invalid scale type!')

            # Handle scale type
            if not scale_type_error:
                scale_position_error = True  # Need to be firstly True for try...exception work
                scale_position = int(input('\nScale position to use: \n1) Root position\n2) 1st inversion\n3) 2nd inversion\nOption: '))
                if 1 <= scale_position <= 3:
                    for note in note_to_scale:
                        # Make chord for each node found on note_to_scale array
                        result.update({
                            note: make_chord([], note, chords_list[scale_type - 1][scale_position - 1], all_notes)
                        })
                    break
                else:
                    print('Invalid scale position!')
        except ValueError:
            print('Insert a valid number!')
    return result, chords_list[scale_type - 1][scale_position - 1]


#
def make_diatonic_scale(scale, index_note, octave, diatonic_scale, all_notes):
    """ Make a diatonic scale.

    Parameters:
    scale : LIST diatonic scale result.
    index_note : INT index on natural notes.
    octave : INT current octave.
    diatonic_scale : INT mode of selected diatonic scales.
    all_notes : LIST all chromatic scale.

    Return type:
    LIST of diatonic scale with octaves an accidents.

    Description:
    Make a diatonic scale to use with Fibonacci sequence.
    """
    # First: Put previous scale note
    index_first_note = index_note - diatonic_scale[-1]
    scale.append(all_notes[index_first_note])

    if index_first_note < 0:
        # Fix note octave
        if len(scale[0]) == 1:
            scale[0] = scale[0][0] + f'{octave - 1}'
        else:
            scale[0] = scale[0][0] + f'{octave - 1}#'
    else:
        # Keep note octave
        if len(scale[0]) == 1:
            scale[0] = scale[0][0] + f'{octave}'
        else:
            scale[0] = scale[0][0] + f'{octave}#'

    # Second: Put natural note
    scale.append(all_notes[index_note])  # Put first note on scale array
    if len(scale[1]) == 1:
        scale[1] = scale[1][0] + f'{octave}'
    else:
        scale[1] = scale[1][0] + f'{octave}#'

    scale_index = 2  # Two first notes already defined

    # Third: Put all notes in selected scale
    for index in diatonic_scale:
        # Calculate what will be the next index
        index_next_note = index_note + index

        # Fix the next index if exceed all_notes length
        if index_next_note >= len(all_notes):
            octave += 1  # Change current octave
            index_next_note -= len(all_notes)

        next_note = all_notes[index_next_note]

        scale.append(next_note)  # Add next note to scale array

        # Fix note octave
        if len(scale[scale_index]) == 1:
            scale[scale_index] = scale[scale_index][0] + f'{octave}'
        else:
            scale[scale_index] = scale[scale_index][0] + f'{octave}#'

        scale_index += 1  # Increase scale index
        index_note = all_notes.index(next_note)  # Receive current index on all_notes array

    # Fourth: Put the next and final scale note
    index_next_note = index_note + diatonic_scale[0]

    if index_next_note >= len(all_notes):
        # Fix the next index and octave if exceed all_notes length
        octave += 1  # Change current octave
        index_next_note -= len(all_notes)

    scale.append(all_notes[index_next_note])

    if len(scale[scale_index]) == 1:
        scale[scale_index] = scale[scale_index][0] + f'{octave}'
    else:
        scale[scale_index] = scale[scale_index][0] + f'{octave}#'
    return scale


def fibonacci_builder(error, result):
    """ Build the Fibonacci sequence.

    Parameters:
    error : STRING error string.
    result : DICTIONARY Fibonacci sequence dictionary (hash table).

    Return type:
    DICTIONARY of Fibonacci sequence (hash table) that starts at 0.

    Description:
    Build the Fibonacci sequence on a dictionary (hash table).
    """
    if error:
        print(error)
    try:
        fib_max = int(input('\nHow many Fibonacci numbers (number > 1): '))
        if fib_max <= 1:
            result = fibonacci_builder('Number is to short!', result)
        elif fib_max > 1:
            print('Calculating the first', fib_max, 'numbers. Please wait...')
            result = fibonacci(fib_max, 0, {0: "0", 1: "1"}, None)
    except RecursionError:
        result = fibonacci_builder('Number is to big!', result)
    except ValueError:
        result = fibonacci_builder('Insert a valid number!', result)
    return result


def create_track(bpm, time_sig, pitches):
    """ Create a single MIDI track.

    Parameters:
    bpm : INT song's beats per minute.
    time_sig : INT song's time signature.
    pitches : LIST notes with octaves and accidents.

    Return type:
    music21.stream of notes (MIDI track).

    Description:
    Create a single MIDI track using music21.stream.
    """
    # Create a stream of notes
    stream = music21.stream.Stream()
    instrument = music21.instrument.Piano()
    stream.append(instrument)

    # Set the stream's tempo
    stream.insert(0, music21.tempo.MetronomeMark(number=bpm))

    # Set the stream's time signature
    stream.insert(0, music21.meter.TimeSignature(f'{time_sig}'))

    # Add notes to stream
    for pitch in pitches:
        if len(pitch[0]) > 2:
            # Chord
            stream.append(music21.chord.Chord(pitch[0], quarterLength=pitch[1]))
        else:
            # Single note
            stream.append(music21.note.Note(pitch[0], quarterLength=pitch[1]))
    return stream


def make_pitches(fibonacci_pitches, golden_ratio_pitches, sequences_dictionary, notes_generated, l_chords, inversion, notes_bar, notes_time):
    """ Make pitches.

    Parameters:
    fibonacci_pitches : LIST Fibonacci pitches.
    golden_ratio_pitches : LIST Golden Ratio pitches.
    sequences_dictionary[0] : DICTIONARY Fibonacci sequence.
    sequences_dictionary[1] : DICTIONARY Golden Ratio sequence.
    notes_generated[0] : LIST diatonic scale of right hand.
    notes_generated[1] : LIST diatonic scale of left hand.
    l_chords : LIST all chord used on left hand.
    inversion : LIST chord position/pattern or triad inversion used on chords.
    notes_bar : INT noter per bar
    notes_time : LIST default Fibonacci and Golden Ratio sequences timers.

    Return type:
    LIST of Fibonacci and Golden Ratio pitches.

    Description:
    Make all notes pitches with a given notes and a sequence.
    """
    notes_number = 1
    golden_ratio_note_time = notes_time[1]
    golden_index = random.randint(0, len(sequences_dictionary[1][0]) - 1)  # Random PHI number
    for i in sequences_dictionary[0]:
        for j in sequences_dictionary[0][i]:
            if notes_number == 1:
                while True:
                    while True:
                        golden_incr, rand_index = 0, random.randint(1, 2)
                        for x in reversed(range(rand_index + 1)):
                            golden_incr += inversion[x]
                        break
                    golden_index_new = golden_index + golden_incr
                    while golden_index >= len(sequences_dictionary[1][0]):
                        golden_index = random.randint(0, len(sequences_dictionary[1][0]) - 1)  # Random PHI number
                    while golden_index_new >= len(sequences_dictionary[1][0]):
                        golden_index_new -= len(sequences_dictionary[1][0])
                    pitch_phi = sequences_dictionary[1][0][golden_index]  # Get the PHI random number
                    pitch_phi_new = sequences_dictionary[1][0][golden_index_new]  # Get the PHI random number
                    if pitch_phi != '.' and pitch_phi_new != '.':
                        first_chord_note = notes_generated[1][int(pitch_phi)]
                        notes_chords = l_chords[first_chord_note]
                        golden_ratio_pitches.append([notes_chords, golden_ratio_note_time])
                        if golden_ratio_note_time == notes_time[1]:
                            golden_ratio_note_time /= 2  # Half note
                        else:
                            first_chord_note_new = notes_generated[1][int(pitch_phi_new)]
                            notes_chords_new = l_chords[first_chord_note_new]
                            golden_ratio_pitches.append([notes_chords_new, golden_ratio_note_time])  # Add one more
                            golden_ratio_note_time *= 2  # Put note back
                        break
                    else:
                        golden_index += 1  # Ignore '.'
                golden_index += 1
            if notes_number == notes_bar:
                notes_number = 1  # Reset notes_number
            else:
                notes_number += 1
            fibonacci_pitches.append([notes_generated[0][int(j)], notes_time[0]])  # Add note to fibonacci_pitches array
    return fibonacci_pitches, golden_ratio_pitches


def make_chord(chord_result, start_note, chord_selected, all_notes):
    """ Make a chord.

    Parameters:
    chord_result : LIST result chord.
    start_note : STRING chord's primary note.
    chord_selected : LIST position/pattern chord selected.
    all_notes : LIST all natural notes.

    Return type:
    LIST of chord based on the given note and position/pattern.

    Description:
    Make a chord based on a given note and position/pattern.
    """
    if len(start_note) == 3:
        chord_note = all_notes.index(start_note[0] + start_note[2])
    else:
        chord_note = all_notes.index(start_note[0])
    note_octave = int(start_note[1])
    for position in chord_selected:
        chord_note += position
        if chord_note >= len(all_notes):
            note_octave += 1
            chord_note -= len(all_notes)
        if len(all_notes[chord_note]) == 1:
            chord_result.append(all_notes[chord_note][0] + f'{note_octave}')
        else:
            chord_result.append(all_notes[chord_note][0] + f'{note_octave}#')
    return chord_result


def create_file(midi_file, filename):
    """ Create a MIDI file.

    Parameters:
    midi_file : music21.midi.MidiFile MIDI content.
    filename : STRING Name of the file.

    Description:
    Create a MIDI file with a given content.
    """
    midi_file.open(f'{filename}', 'wb')
    midi_file.write()
    midi_file.close()
    print('File created!')


if __name__ == '__main__':
    # Diatonic scales
    diatonic_scales = {
        0: [2, 2, 1, 2, 2, 2, 1],  # Ionico
        1: [2, 1, 2, 2, 2, 1, 2],  # Dorico
        2: [1, 2, 2, 2, 1, 2, 2],  # Frigio
        3: [2, 2, 2, 1, 2, 2, 1],  # Lidio
        4: [2, 2, 1, 2, 2, 1, 2],  # Misolidio
        5: [2, 1, 2, 2, 1, 2, 2],  # Eolico
        6: [1, 2, 2, 1, 2, 2, 2]  # Locrio
    }

    # Chords positions/patterns and triad inversion
    chords_and_inversion = {
        # Major chords
        0: {
            0: [0, 4, 3],  # Root position
            1: [4, 3, 5],  # 1st inversion
            2: [7, 5, 4]  # 2nd inversion
        },
        # Minor chords
        1: {
            0: [0, 3, 4],  # Root position
            1: [3, 4, 5],  # 1st inversion
            2: [7, 5, 3]  # 2nd inversion
        },
        # Diminished chord
        2: {
            0: [0, 3, 3],  # Root position
            1: [3, 3, 6],  # 1st inversion
            2: [6, 6, 3]  # 2nd inversion
        },
        # Augmented chord
        3: {
            0: [0, 4, 4],  # Root position
            1: [4, 4, 4],  # 1st inversion
            2: [8, 4, 4]  # 2nd inversion
        }
    }

    # Chords left hand (Piano)
    l_piano_chords = {}

    # Important information
    current_octave = 4
    filename_midi = 'fibonacci.mid'

    # Useful array
    all_tracks = []

    # Chromatic Scale
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Define beats per minute
    while True:
        try:
            beats_per_minute = int(input('Beats per minute to use (BPM): '))
            break
        except ValueError:
            print('\nInsert a valid number!')

    # Get time signature, notes per bar and the sequences timers
    time_signature, notes_per_bar, sequence_timers = make_time_signature()

    # Get the diatonic mode to use on MIDI project
    diatonic_mode = diatonic_selection(diatonic_scales, '', None)

    # Select scale to use the previous diatonic mode
    while True:
        try:
            print('\nScales available: ', chromatic_scale)
            scale_to_use = input('Scale to use: ').upper()
            index_scale_note = chromatic_scale.index(scale_to_use)  # Receive index number from all_notes array
            break
        except ValueError:
            print('Invalid note!')

    # Get all notes on right hand (Piano)
    r_piano = make_diatonic_scale([], index_scale_note, current_octave, diatonic_mode, chromatic_scale)

    # Get all notes on left hand (Piano)
    current_octave -= 2
    l_piano = make_diatonic_scale([], index_scale_note, current_octave, diatonic_mode, chromatic_scale)

    # Calculate chords for all notes available on left hand (Piano)
    l_piano_chords, inversion_used = chord_type({}, l_piano, chords_and_inversion, False, False, chromatic_scale)

    # Show some useful information to the user
    print(f'\nScales in use:')
    print(f'\t{scale_to_use} scale (Octave {current_octave}):', r_piano)
    print(f'\t{scale_to_use} scale (Octave {current_octave}):', l_piano)
    print('\n{scale_to_use} scale chords That will be used on left hand:')
    for chords in l_piano_chords:
        print(f'\t{chords}:', l_piano_chords[chords])

    # Build some calculations [Fibonacci sequence, Golden Ratio]
    fib, golden_ratio = fibonacci_builder('', None), {0: str((1 + sqrt(5)) / 2)}

    # Determine the pitches notes based on Fibonacci sequence and Golden Ratio
    notes_pitches = make_pitches([], [], [fib, golden_ratio], [r_piano, l_piano], l_piano_chords, inversion_used, notes_per_bar, sequence_timers)

    # Create MIDI tracks
    print('Creating stream. Please wait...')
    for notes_pitch in notes_pitches:
        all_tracks.append(create_track(beats_per_minute, time_signature, notes_pitch))

    # Create score to put all MIDI tracks together
    score = music21.stream.Score()
    for track in all_tracks:
        score.insert(track)

    # Convert music21.stream to MIDI format
    print('Converting stream to MIDI format. Please wait...')
    final_midi = music21.midi.translate.streamToMidiFile(score)
    
    # Write the produced MIDI format
    print('Creating file', filename_midi)
    create_file(final_midi, filename_midi)
