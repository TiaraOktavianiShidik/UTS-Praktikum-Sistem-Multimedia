from flask import Flask, render_template, request
import os
import librosa
import soundfile as sf
# import subprocess
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    # Ambil file audio yang diunggah dari form
    audio = request.files['audio']

    # Simpan file audio yang diunggah di folder uploads
    audio_path = f'static/uploads/{audio.filename}'
    audio.save(audio_path)

    # Load file audio menggunakan soundfile
    data, sample_rate = sf.read(audio_path)

    # Kompresi audio dengan mengurangi bitrate
    compressed_data = data / 2  # Contoh sederhana: Mengurangi bitrate setengahnya

    # Path untuk file audio hasil kompresi
    compressed_audio_path = f'static/uploads/compressed_{audio.filename}'

    # Simpan audio hasil kompresi
    sf.write(compressed_audio_path, compressed_data, sample_rate)

    # Hapus file audio asli
    # os.remove(audio_path)

    # Render halaman hasil kompresi dengan menampilkan file audio asli dan hasil kompresi
    return render_template('result-compress.html', original_audio=audio.filename, compressed_audio=f'compressed_{audio.filename}')


@app.route('/process', methods=['POST'])
def process():
    # Ambil file audio yang diunggah dari form
    audio = request.files['audio']

    # Simpan file audio yang diunggah di folder uploads
    filename = audio.filename
    audio_path = os.path.join('static/uploads', filename)
    audio.save(audio_path)

    # Load audio menggunakan library librosa
    audio_data, sample_rate = librosa.load(audio_path)

    # Lakukan pemrosesan efek suara di sini menggunakan library dan algoritma yang sesuai
    # Contoh: Melakukan perubahan pitch menggunakan algoritma Time Stretching pada library librosa
    audio_stretch = librosa.effects.time_stretch(audio_data, rate=0.8)

    # Path untuk file audio hasil pemrosesan efek suara
    processed_filename = f'processed_{filename}'
    processed_audio_path = os.path.join('static/uploads', processed_filename)

    # Simpan file audio hasil pemrosesan
    sf.write(processed_audio_path, audio_stretch, sample_rate)

    # Hapus file asli yang diunggah
    # os.remove(audio_path)

    # Render halaman hasil pemrosesan dengan menampilkan file audio asli dan hasil pemrosesan
    return render_template('result-process.html', original_audio=filename, processed_audio=processed_filename)
