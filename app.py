from datetime import datetime, timedelta
import os
from flask import Flask, flash, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

app = Flask(__name__)
app.secret_key = 'Project-DTS-Group-6'      # Secret key
app.config['SAVE_IMAGE'] = 'uploads/img/'   # Folder image
app.config['SAVE_DOCX'] = 'uploads/docx/'   # Folder docx

#fungsi untuk mengkonversi setiap elemen menjadi array of object
def toArrayObj(thn, act):
    hasil = []
    for x in range(len(thn)):
        temp = {}
        temp['tahun'] = thn[x]
        temp['nama'] = act[x]
        hasil.append(temp)

    return hasil

# Fungsi filter matching extension gambar
def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'gif']

# Route halaman awal
@app.route('/')
def index():
    # Hapus file jika file sudah 2 menit
    for file in os.listdir(app.config['SAVE_DOCX']): #lihat semua file yang ada di folder uploads/docx
        #cek waktu dibuatnya tiap-tiap file 
        if datetime.now() - datetime.fromtimestamp(os.path.getctime(os.path.join(app.config['SAVE_DOCX'], file))) >= timedelta(minutes=2):
                #jika waktu file dibuat lebih dari 2 menit dari waktu sekarang, maka hapus file
                os.remove(os.path.join(app.config['SAVE_DOCX'], file))
    # Tampilkan halaman awal
    return render_template('index.html', title='Dashboard')

#Route halaman buat CV
@app.route('/buat_cv', methods=['POST', 'GET'])
def buat_cv():
    # Jika request POST
    if request.method == 'POST':
        try:
            # Data form dan gambar dari user disimpan ke variabel
            form = request.form
            photo = request.files['photo']

            #Inisialisasi nama file
            nama_file = datetime.now().strftime("%d%m%Y_%H%M%S_") + request.form['nama'].split(' ')[-1] + '.'

            # Upload photo
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)      # Cek apakah file berbahaya (Flask merekomendasikan ini)
                extension = filename.split('.')[-1]             # Ambil extensi foto misalnya jpg, png, gif.
                photo.filename = nama_file + extension          # Ubah nama file/photo
                photo.save(os.path.join(app.config['SAVE_IMAGE'], photo.filename))  # Simpan foto ke folder uploads/img

            # Setting ukuran poto berdasarkan design yg dipilih user
            if form['design'] == '1':
                width = 60.3
            elif form['design'] == '2':
                width = 69.2
            elif form['design'] == '3':
                width = 77.3
            else:
                width = 55.5

            # Buka file template CV docx berdasarkan design yg dipilih user
            tCV = DocxTemplate("./templates/docx/CV"+form['design']+".docx")

            #konversi semua data form menjadi dict
            data = {
                "nama_lengkap" : form['nama'],
                "tgl_lahir": form['tgl_lahir'].split('-'),
                "tempat_lahir": form['tempat_lahir'],
                "alamat": form['alamat'],
                "photo": InlineImage(tCV, app.config['SAVE_IMAGE'] + photo.filename, width=Mm(width), height=Mm(width)),
                "email" : form['email'],
                "no_hp" : form['no_hp'],
                "skills": form.getlist('keahlian'),
                "pendidikan" : toArrayObj(form.getlist('thn_pend'), form.getlist('pendidikan')),
                "pengalaman" : toArrayObj(form.getlist('thn_peng'), form.getlist('pengalaman')),
                "social" : form['social'],
                "bio" : form['bio']
            }

            tCV.render(data) #Render data ke template
            tCV.save(os.path.join(app.config['SAVE_DOCX'], nama_file + "docx")) # Simpan file docx

            #hapus foto agar tidak overload server
            os.remove(os.path.join(app.config['SAVE_IMAGE'], photo.filename))

            #pesan berhasil
            flash('Yeay, CV kamu berhasil dibuat!', category='success')

            #tampilkan halaman buat cv dengan membawa nama file
            return render_template('buat_cv.html', title='Buat CV', filename=nama_file+"docx")
        except:
            #hapus foto berbahaya
            os.remove(os.path.join(app.config['SAVE_IMAGE'], photo.filename))
            #pesan peringatan
            flash('File foto berbahaya! mohon ganti foto lain', category='danger')

    #tampilkan halaman buat cv pada method GET
    return render_template('buat_cv.html', title='Buat CV')

#Route untuk download hasil CV
@app.route('/download/<namafile>')
def download_file(namafile):
    return send_from_directory(app.config["SAVE_DOCX"], namafile)

if __name__ == "__main__":
    app.run()