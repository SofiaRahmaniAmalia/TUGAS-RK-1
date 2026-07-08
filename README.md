# Kamus Bahasa Sunda dengan Algoritma Genetika

Implementasi Algoritma Genetika (Genetic Algorithm) untuk pencarian kata dalam kamus bahasa daerah Sunda.

## Cara Menjalankan

```bash
python3 kamus_sunda.py
```

## Menu Program

1. Tampilkan Kamus
2. Cari Kata
3. Jalankan Algoritma Genetika
4. Tampilkan Populasi
5. Hasil Fitness
6. Seleksi Roulette
7. Cross Over
8. Mutasi
9. Generasi Baru
10. Keluar

## Cara Menjalankan Demo (1 generasi, deterministik)

```bash
python3 demo_satu_generasi.py
```

Script ini mencetak langkah demi langkah perhitungan fitness, seleksi roulette,
crossover, mutasi, dan generasi baru untuk kata target `"cai"` (artinya "air"),
menggunakan seed acak tetap (`random.seed(42)`) agar hasilnya dapat direproduksi.

## Isi Repository

- `kamus_sunda_ga.py` — Program utama (menu interaktif).
- `demo_satu_generasi.py` — Demo perhitungan 1 generasi GA (untuk laporan).
- `Laporan_GA_Kamus_Sunda.docx` — Laporan tugas.

## Catatan Sebelum Dikumpulkan

- Ganti `[ISI NAMA ANDA]`, `[ISI NIM ANDA]`, dan `[ISI LINK GITHUB ANDA]` di
  dalam laporan dengan data Anda sendiri.
- Disarankan mengambil screenshot langsung dari environment Anda sendiri saat
  menjalankan program (bukan hanya menggunakan gambar contoh yang disediakan),
  agar sesuai dengan ketentuan orisinalitas tugas.
- Jangan lupa push source code ke GitHub dan sertakan link-nya di laporan
  serta di link pengumpulan.
