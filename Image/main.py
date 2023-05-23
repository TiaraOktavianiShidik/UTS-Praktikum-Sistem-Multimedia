from flask import Flask, render_template, request
import os
from PIL import Image, ImageFilter

app=Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/compress', methods=['POST'])
def compress():
    # Ambil file gambar yang diunggah dari form
    image = request.files['image']

    # Simpan gambar yang diunggah di folder uploads
    filename = image.filename
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Path untuk gambar hasil kompresi
    compressed_filename = f'compressed_{filename}'
    compressed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)

    # Lakukan kompresi gambar menggunakan PIL
    img = Image.open(image_path)
    img.save(compressed_image_path, optimize=True, quality=50)

    # Render halaman hasil kompresi dengan menampilkan gambar asli dan hasil kompresi
    return render_template('result-compress.html', original_image=filename, compressed_image=compressed_filename)

@app.route('/process', methods=['POST'])
def process():
    # Ambil file gambar yang diunggah dari form
    image = request.files['image']

    # Simpan gambar yang diunggah di folder uploads
    filename = image.filename
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Path untuk gambar hasil proses
    processed_filename = f'processed_{filename}'
    processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

    # Lakukan image processing dengan memberikan filter menggunakan PIL
    img = Image.open(image_path)
    img = img.filter(ImageFilter.GaussianBlur(radius=10))
    img.save(processed_image_path)

    # Render halaman hasil proses dengan menampilkan gambar asli dan gambar hasil proses
    return render_template('result-process.html', original_image=filename, processed_image=processed_filename)
