from flask import Flask, request, send_from_directory
import os
from midigen.complex_midigen import accept_external_note_data

app = Flask(__name__)

midi_output_dir = '/var/www/midigen'  # Set the output directory for MIDI files

@app.route('/generate_midi', methods=['POST'])
def generate_midi():
    # Extract notes data from request
    data = request.json
    notes = data.get('notes', [])
    print("Received notes data:", notes)  # Log received data

    # Generate MIDI file using the refactored script
    try:
        filename = accept_external_note_data(notes, output_dir=midi_output_dir)
        # The above function call should be modified to accept an output directory
        file_path = os.path.join(midi_output_dir, filename)
        if os.path.exists(file_path):
            print(f"MIDI file generated at {file_path}")
        else:
            print(f"Failed to locate MIDI file at {file_path}")
        return {'message': 'MIDI file generated successfully', 'filename': filename}
    except Exception as e:
        print(f"Error during MIDI file generation: {e}")
        return {'error': str(e)}, 400

@app.route('/midi/<filename>')
def get_midi(filename):
    return send_from_directory(midi_output_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
