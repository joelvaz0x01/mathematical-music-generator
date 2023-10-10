import random
import music21
from math import log2


def fibonacci(num, count, hash_list, result):
    """
    Calculate the first 'num' numbers of Fibonacci sequence using functional programing.
    :param num: INT maximum number to calculate the Fibonacci sequence.
    :param count: INT auxiliary variable that helps to build the Fibonacci sequence.
    :param hash_list: DICTIONARY result of Fibonacci sequence (hash table).
    :param result: DICTIONARY result of Fibonacci sequence (hash table).
    :return: DICTIONARY that contains the first 'num' numbers of Fibonacci sequence.
    """
    if num == count + 2:
        result = hash_list
    else:
        tmp_res = int(hash_list[count]) + int(hash_list[count + 1])
        hash_list.update({count + 2: str(tmp_res)})
        result = fibonacci(num, count + 1, hash_list, result)

    return result


def diatonic_selection(diatonic_scale, error, result):
    """
    Select a diatonic scale to use as base.
    :param diatonic_scale: DICTIONARY all diatonic scales (hash table).
    :param error: STRING error string.
    :param result: LIST selected diatonic mode.
    :return: LIST of position/pattern of the selected diatonic mode.
    """
    if error:
        print(error)

    try:
        mode = int(
            input(
                'Diatonic scale to use:\n'
                '1) Ionico\n'
                '2) Dorico\n'
                '3) Frigio\n'
                '4) Lidio\n'
                '5) Misolidio\n'
                '6) Eolico\n'
                '7) Locrio\n'
                'Option: '
            )
        )
        if 1 <= mode <= 7:
            result = list(diatonic_scale.values())[mode - 1]
        else:
            result = diatonic_selection(diatonic_scale, 'Invalid mode!', result)
    except ValueError:
        result = diatonic_selection(diatonic_scale, 'Insert a valid number!', result)

    return result


def make_time_signature():
    """
    Make and verify if is valid the time signature, notes per bar and the default Fibonacci and Golden Ratio sequences timers.
    :return: LIST of the final time signature, the maximum notes in bars and the sequences timers.
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
    print(f'\nTime signature that will be used: {time_sig}\n')

    return time_sig, notes_bar, [fibonacci_note_time, golden_ratio_note_time]


def chord_type(result, note_to_scale, chords_list, scale_type_error, scale_position_error, all_notes):
    """
    Make chords or triad inversion with a given list of notes.
    :param result: LIST result notes in chord (three notes).
    :param note_to_scale: LIST all notes to make a chord or a triad inversion.
    :param chords_list: LIST all chords positions/patterns or triad inversions.
    :param scale_type_error: BOOLEAN scale type error.
    :param scale_position_error: BOOLEAN scale position/pattern error.
    :param all_notes: LIST all chromatic scale.
    :return: LIST of notes in chord and the chord position/pattern or triad inversion used.
    """
    scale_type, scale_position = 0, 0
    while True:
        try:
            # handle scale position
            if not scale_position_error:
                scale_type_error = True  # need to be firstly True for `try ... exception` work
                scale_type = int(
                    input(
                        '\nScale type to use:'
                        '\n1) Major chords'
                        '\n2) Minor chords'
                        '\n3) Diminished chord'
                        '\n4) Augmented chord'
                        '\nOption: '
                    )
                )
                if 1 <= scale_type <= 4:
                    scale_type_error = False
                else:
                    print('Invalid scale type!')

            # handle scale type
            if not scale_type_error:
                scale_position_error = True  # need to be firstly True for `try ... exception` work
                scale_position = int(
                    input(
                        '\nScale position to use:'
                        '\n1) Root position'
                        '\n2) 1st inversion'
                        '\n3) 2nd inversion'
                        '\nOption: '
                    )
                )
                if 1 <= scale_position <= 3:
                    for note in note_to_scale:
                        # make chord for each node found on `note_to_scale` array
                        result.update({
                            note: make_chord([], note, chords_list[scale_type - 1][scale_position - 1], all_notes)
                        })
                    break
                else:
                    print('Invalid scale position!')
        except ValueError:
            print('Insert a valid number!')

    return result, chords_list[scale_type - 1][scale_position - 1]


def make_diatonic_scale(scale, index_note, octave, diatonic_scale, all_notes):
    """
    Make a diatonic scale to use with Fibonacci sequence.
    :param scale: LIST diatonic scale result.
    :param index_note: INT index on natural notes.
    :param octave: INT current octave.
    :param diatonic_scale: INT mode of selected diatonic scales.
    :param all_notes: LIST all chromatic scale.
    :return: LIST of diatonic scale with octaves an accidents.
    """
    # first: put previous scale note
    index_first_note = index_note - diatonic_scale[-1]
    scale.append(all_notes[index_first_note])

    if index_first_note < 0:
        # fix note octave
        if len(scale[0]) == 1:
            scale[0] = scale[0][0] + f'{octave - 1}'
        else:
            scale[0] = scale[0][0] + f'{octave - 1}#'
    else:
        # keep note octave
        if len(scale[0]) == 1:
            scale[0] = scale[0][0] + f'{octave}'
        else:
            scale[0] = scale[0][0] + f'{octave}#'

    # second: put natural note
    scale.append(all_notes[index_note])  # put first note on scale array
    if len(scale[1]) == 1:
        scale[1] = scale[1][0] + f'{octave}'
    else:
        scale[1] = scale[1][0] + f'{octave}#'

    scale_index = 2  # two first notes already defined

    # third: put all notes in selected scale
    for index in diatonic_scale:
        # calculate what will be the next index
        index_next_note = index_note + index

        # fix the next index if exceed `all_notes` array length
        if index_next_note >= len(all_notes):
            octave += 1  # change current octave
            index_next_note -= len(all_notes)

        next_note = all_notes[index_next_note]

        scale.append(next_note)  # add next note to scale array

        # fix note octave
        if len(scale[scale_index]) == 1:
            scale[scale_index] = scale[scale_index][0] + f'{octave}'
        else:
            scale[scale_index] = scale[scale_index][0] + f'{octave}#'

        scale_index += 1  # increase scale index
        index_note = all_notes.index(next_note)  # receive current index on `all_notes` array

    # fourth: put the next and final scale note
    index_next_note = index_note + diatonic_scale[0]

    if index_next_note >= len(all_notes):
        # fix the next index and octave if exceed `all_notes` array length
        octave += 1  # change current octave
        index_next_note -= len(all_notes)

    scale.append(all_notes[index_next_note])

    if len(scale[scale_index]) == 1:
        scale[scale_index] = scale[scale_index][0] + f'{octave}'
    else:
        scale[scale_index] = scale[scale_index][0] + f'{octave}#'

    return scale


def fibonacci_builder(error, result):
    """
    Build the Fibonacci sequence on a dictionary (hash table).
    :param error: STRING error string.
    :param result: DICTIONARY Fibonacci sequence dictionary (hash table).
    :return: DICTIONARY of Fibonacci sequence (hash table) that starts at 0.
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
    """
    Create a single MIDI track using music21.stream.
    :param bpm: INT song's beats per minute.
    :param time_sig: INT song's time signature.
    :param pitches: LIST notes with octaves and accidents.
    :return: music21.stream of notes (MIDI track).
    """
    # create a stream of notes
    stream = music21.stream.Stream()
    instrument = music21.instrument.Piano()
    stream.append(instrument)

    # set the stream's tempo
    stream.insert(0, music21.tempo.MetronomeMark(number=bpm))

    # set the stream's time signature
    stream.insert(0, music21.meter.TimeSignature(f'{time_sig}'))

    # add notes to stream
    for pitch in pitches:
        if len(pitch[0]) > 2:
            # chord
            stream.append(music21.chord.Chord(pitch[0], quarterLength=pitch[1]))
        else:
            # single note
            stream.append(music21.note.Note(pitch[0], quarterLength=pitch[1]))

    return stream


def make_pitches(fibonacci_pitches, golden_ratio_pitches, sequences_dictionary, notes_generated, l_chords, inversion,
                 notes_bar, notes_time):
    """
    Make all notes pitches with a given notes and a sequence.
    :param fibonacci_pitches: LIST Fibonacci pitches.
    :param golden_ratio_pitches: LIST Golden Ratio pitches.
    :param sequences_dictionary: DICTIONARY Fibonacci and Golden Ratio sequences.
    :param notes_generated: LIST diatonic scale of right hand.
    :param l_chords: LIST all chord used on left hand.
    :param inversion: LIST chord position/pattern or triad inversion used on chords.
    :param notes_bar: INT noter per bar
    :param notes_time: LIST default Fibonacci and Golden Ratio sequences timers.
    :return: LIST of Fibonacci and Golden Ratio pitches.
    """
    notes_number = 1
    golden_ratio_note_time = notes_time[1]
    golden_index = random.randint(0, len(sequences_dictionary[1][0]) - 1)  # random PHI number
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
                        golden_index = random.randint(0, len(sequences_dictionary[1][0]) - 1)  # random PHI number
                    while golden_index_new >= len(sequences_dictionary[1][0]):
                        golden_index_new -= len(sequences_dictionary[1][0])
                    pitch_phi = sequences_dictionary[1][0][golden_index]  # get the PHI random number
                    pitch_phi_new = sequences_dictionary[1][0][golden_index_new]  # get the PHI random number
                    if pitch_phi != '.' and pitch_phi_new != '.':
                        first_chord_note = notes_generated[1][int(pitch_phi)]
                        notes_chords = l_chords[first_chord_note]
                        golden_ratio_pitches.append([notes_chords, golden_ratio_note_time])
                        if golden_ratio_note_time == notes_time[1]:
                            golden_ratio_note_time /= 2  # half note
                        else:
                            first_chord_note_new = notes_generated[1][int(pitch_phi_new)]
                            notes_chords_new = l_chords[first_chord_note_new]
                            golden_ratio_pitches.append([notes_chords_new, golden_ratio_note_time])  # add one more
                            golden_ratio_note_time *= 2  # put note back
                        break
                    else:
                        # ignore '.'
                        golden_index += 1
                golden_index += 1
            if notes_number == notes_bar:
                # reset `notes_number` variable
                notes_number = 1
            else:
                notes_number += 1

            # add note to `fibonacci_pitches` array
            fibonacci_pitches.append([notes_generated[0][int(j)], notes_time[0]])

    return fibonacci_pitches, golden_ratio_pitches


def make_chord(chord_result, start_note, chord_selected, all_notes):
    """
    Make a chord based on a given note and position/pattern.
    :param chord_result: LIST result chord.
    :param start_note: STRING chord's primary note.
    :param chord_selected: LIST position/pattern chord selected.
    :param all_notes: LIST all natural notes.
    :return: LIST of chord based on the given note and position/pattern.
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
    """
    Create a MIDI file with a given content.
    :param midi_file: music21.midi.MidiFile MIDI content.
    :param filename: STRING Name of the file.
    :return: None
    """
    midi_file.open(f'{filename}', 'wb')
    midi_file.write()
    midi_file.close()
    print('File created!')
