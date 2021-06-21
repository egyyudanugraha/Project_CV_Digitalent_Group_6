let i = 1;
function tambahKeahlian() {
    const div = document.createElement('div');
    div.className = 'row';
    
    div.innerHTML = `
    <div class="col-md-12">
        <label class="labels">Keahlian</label>
        <a style="cursor: pointer;" onclick="hapusKeahlian(this)" class="labels float-end mt-1 text-decoration-none">Hapus</a>
        <input type="text" name="keahlian" class="form-control" placeholder="Keahlian">
    </div>
    `;
    if(i <= 3){
        document.querySelector('.p-3 > .row > .p-3 > .col-md-12').appendChild(div);
        i++
    }
}
    
function hapusKeahlian(input) {
    document.querySelector('.p-3 > .row > .p-3 > .col-md-12').removeChild(input.parentNode.parentNode);
    i--
}

let u = 1;
function tambahPendidikan() {
    const div = document.createElement('div');
    div.className = 'row';
    
    div.innerHTML = `
            <div class="col-md-9">
                <label class="labels">Pendidikan</label>
                <a style="cursor: pointer;" onclick="hapusPendidikan(this)" class="labels float-end mt-1 text-decoration-none">Hapus</a>
                <input type="text" name="pendidikan" class="form-control" placeholder="Pendidikan dasar">
            </div>
            <div class="col-md-3">
                <label class="labels">Tahun lulus</label>
                <input type="text" name="thn_pend" class="form-control" placeholder="Tahun">
            </div>
    `;
    if(u <= 2){
        document.querySelector('.col-md-5 > .pend').appendChild(div);
        u++
    }
}
    
function hapusPendidikan(input) {
    document.querySelector('.col-md-5 > .pend').removeChild(input.parentNode.parentNode);
    u--
}

let o = 1;
function tambahPengalaman() {
    const div = document.createElement('div');
    div.className = 'row';
    
    div.innerHTML = `
        <div class="col-md-9">
            <label class="labels">Pengalaman</label>
            <a style="cursor: pointer;" onclick="hapusPengalaman(this)" class="labels float-end mt-1 text-decoration-none">Hapus</a>
            <input type="text" name="pengalaman" class="form-control" placeholder="Pengalaman" required>
        </div>
        <div class="col-md-3">
            <label class="labels">Tahun</label>
            <input type="text" name="thn_peng" class="form-control" placeholder="Tahun" required>
        </div>
    `;
    if(o <= 2){
        document.querySelector('.row > .col-md-5 > .peng').appendChild(div);
        o++
    }
}
    
function hapusPengalaman(input) {
    document.querySelector('.row > .col-md-5 > .peng').removeChild(input.parentNode.parentNode);
    o--
}

const input = document.querySelector('#files')
input.onchange = () => {
    const [file] = input.files
    if (file) {
      photo.src = URL.createObjectURL(file)
    }
  }

const form = document.querySelector('#buat_cv');
const btn = document.querySelector('#buat');

form.addEventListener('submit', () => {
    btn.innerHTML = ``;
    btn.innerHTML = `<button class="btn btn-danger" type="button" disabled>
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    CV sedang dibuat...
  </button>`;
})