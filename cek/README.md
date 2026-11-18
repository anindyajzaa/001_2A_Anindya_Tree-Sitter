# cek.py

CLI kecil untuk memeriksa file Python dengan tree-sitter. Program membaca semua file `.py` di sebuah folder, lalu melaporkan:

1. komentar yang berisi `TODO` atau `FIXME`,
2. fungsi yang lebih dari 30 baris,
3. file yang pohonnya mengandung error sintaks.

## Memasang dependensi

Butuh Python 3. Buat virtual environment, aktifkan, lalu pasang paketnya:

```bash
python3 -m venv venv
source venv/bin/activate
pip install tree-sitter tree-sitter-python
```

## Menjalankan

```bash
python cek.py <folder>
```

Contoh, memeriksa folder uji bawaan:

```bash
python cek.py uji
```

Untuk menyimpan hasilnya ke file:

```bash
python cek.py uji > output_uji.txt
```

Folder `venv`, `.git`, dan `node_modules` dilewati. Kalau folder tidak ditemukan, program mencetak pesan dan berhenti.

## Contoh output

Format tiap temuan: `file:baris: keterangan`. Baris terakhir menunjukkan jumlah file yang diperiksa.

```
uji/todo.py:1: # TODO: tambahkan validasi input
uji/todo.py:3: # FIXME: hasilnya salah untuk angka negatif
uji/panjang.py:1: fungsi proses_data terlalu panjang (34 baris)
uji/rusak.py:1: sintaks error
Selesai: 3 file diperiksa
```

Urutan temuan bisa berbeda antar komputer, karena urutan file dibaca dari sistem berkas.

## Cara kerja singkat

- **TODO/FIXME:** query tree-sitter `((comment) @c (#match? @c "TODO|FIXME"))`, jadi hanya komentar yang dihitung. Kata `TODO` di dalam string tidak dilaporkan.
- **Fungsi panjang:** query `(function_definition name: (identifier) @nama) @fungsi`, lalu jumlah baris dihitung dari `end_point` dikurangi `start_point`, ditambah 1. Batasnya 30 baris. Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
- **File error:** memeriksa `root_node.has_error`. Kalau ada, program menelusuri pohon secara rekursif untuk mencari node `ERROR` atau `MISSING` pertama, dan melaporkan barisnya.

## Pengujian

1. **Folder `uji/`:** berisi tiga file buatan sendiri (`todo.py`, `panjang.py`, `rusak.py`). Hasilnya sesuai hitungan manual: 2 komentar TODO/FIXME, 1 fungsi 34 baris, dan 1 file dengan error di baris 1.
2. **Repo nyata:** proyek kuliah Nutri-Kost, 40 file `.py` diperiksa. Contoh temuan fungsi panjang: `_build_ui` (49 baris), `_create_row` (52 baris), `createProfil` (46 baris), dan `calculatorHarrisBenedict` (34 baris). Hasilnya dicocokkan manual pada 2 file: `top_makanan_widget.py` dan `profil_system.py`, dengan membuka file di editor dan menghitung baris awal dan akhir fungsi.

## Keterbatasan

- Hanya mendukung file Python.
- Fungsi dihitung dari baris `def` sampai baris terakhirnya, termasuk baris kosong dan komentar di dalamnya.
- Hanya komentar yang dicek untuk `TODO` dan `FIXME`, jadi hasilnya bisa lebih sedikit daripada `grep`.