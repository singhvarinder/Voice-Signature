# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import simpleaudio as sa
import voice_auth, callrecord

from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'flac'}

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    result = voice_auth.enroll(data['a'], data['b'])
    return jsonify({'result': result})

def enrolluploaded(nm,fname):
    data = request.json
    result = voice_auth.enroll(nm,fname)
    return jsonify({'result': result})

@app.route('/recognize/<string:fname>', methods=['GET'])
def recognize(fname):
    if not fname:
        return jsonify({"Error": "missing user data"})
    fname="./uploads/"+fname
    result = voice_auth.recognize(fname)
    return jsonify({'result': "Hi '" + result + "', how I can help you"})


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("Caller " + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def uploadsimulatecall():
    if request.method == 'POST':
        print("uploading simulator call")
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("Caller " + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/static/action/<filename>')
def action(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Perform some action with the file (e.g., play the audio, analyze it, etc.)
    # Here's an example using pydub to analyze the audio file.
    audio = AudioSegment.from_file(file_path)
    print(file_path)
    duration = audio.duration_seconds
    return f'File: {filename}, Duration: {duration} seconds'

@app.route('/static/play/<filename>', methods=['GET'])
def play_audio(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(file_path):
        return jsonify({'error': 'File not found'}), 404 # Load and play the audio file
    audio = AudioSegment.from_file(file_path)
    play_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    play_obj.wait_done() # Wait until playback is finished
    return  recognize(filename)


@app.route('/record', methods=['POST'])
def record():
    data = request.json
    is_checked = data.get('checked')
    # return jsonify({'checked': is_checked})
    if is_checked:
        callrecord.recordcall()
        return enrolluploaded("Tester","./uploads/sample.flac")
    else:
        callrecord.recordcall()
        return  recognize("sample.flac")

if __name__ == '__main__':
    app.run(port=5000, debug=True)


