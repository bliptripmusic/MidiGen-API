import mido
from mido import Message, MidiFile, MidiTrack
import os

def create_midi_file(filepath, notes, ticks_per_beat):
    print("Creating MIDI file:", filepath)
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    events = []
    for note in notes:
        start_tick = int(note['start_time'] * ticks_per_beat)
        end_tick = start_tick + int(note['duration'] * ticks_per_beat)
        events.append(('note_on', start_tick, note['pitch']))
        events.append(('note_off', end_tick, note['pitch']))

        # Debug print statements
        print(f"Note {note['pitch']}: start_tick = {start_tick}, end_tick = {end_tick}")

    events.sort(key=lambda e: (e[1], e[0] == 'note_off'))

    last_event_time = 0
    for event in events:
        event_type, event_time, pitch = event
        delta_time = event_time - last_event_time
        last_event_time = event_time

        # Debug print statement for delta_time
        print(f"Event {event_type} for Note {pitch}: delta_time = {delta_time}")

        if event_type == 'note_on':
            track.append(Message('note_on', note=pitch, velocity=64, time=delta_time))
        else:
            track.append(Message('note_off', note=pitch, velocity=64, time=delta_time))

    # Save the MIDI file
    mid.save(filepath)
    print("MIDI file saved:", filepath)
    print("File path:", os.path.abspath(filepath))

# Function to accept external note data
def accept_external_note_data(note_data, output_dir):
    filename = 'output.mid'
    filepath = os.path.join(output_dir, filename)
    ticks_per_beat = 480
    create_midi_file(filepath, note_data, ticks_per_beat)
    return filename
