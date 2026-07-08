"""
Demo non-interaktif: menjalankan proses Algoritma Genetika untuk mencari
kata "bumi" (bahasa Sunda Halus, artinya "rumah") secara deterministik
(seed tetap) agar hasilnya bisa direproduksi untuk laporan.
"""
import random
from kamus_sunda_ga import (
    KAMUS_SUNDA, ALPHABET, UKURAN_POPULASI, LAJU_MUTASI,
    buat_populasi_awal, hitung_fitness, evaluasi_populasi,
    seleksi_roulette, crossover_single_point, mutasi
)

random.seed(67)  # seed tetap supaya perhitungan bisa diverifikasi manual

TARGET = "bumi"

print("=" * 60)
print(" DEMO ALGORITMA GENETIKA - PENCARIAN KATA 'bumi' (rumah)")
print("=" * 60)

populasi = buat_populasi_awal(TARGET)
print(f"\nKata target      : '{TARGET}'  (panjang = {len(TARGET)})")
print(f"Ukuran populasi  : {UKURAN_POPULASI}")
print(f"Populasi awal (Generasi ke-1):")
for i, ind in enumerate(populasi, start=1):
    print(f"  Individu {i}: '{ind}'")

# ---------- LANGKAH 1: FITNESS ----------
fitness = evaluasi_populasi(populasi, TARGET)
print("\n--- Langkah 1: Perhitungan Fitness ---")
for i, (ind, f) in enumerate(zip(populasi, fitness), start=1):
    print(f"  Individu {i}: '{ind}' vs target '{TARGET}' -> fitness = {f}/{len(TARGET)}")

# ---------- LANGKAH 2: SELEKSI ROULETTE ----------
print("\n--- Langkah 2: Seleksi Roulette Wheel ---")
bobot = [f + 1 for f in fitness]
total = sum(bobot)
print(f"Total bobot (fitness+1) = {total}")
for i, (ind, b) in enumerate(zip(populasi, bobot), start=1):
    print(f"  Individu {i}: '{ind}' bobot={b} -> probabilitas = {b}/{total} = {b/total:.3f}")

mating_pool, prob = seleksi_roulette(populasi, fitness, UKURAN_POPULASI)
print("\nMating pool hasil seleksi:")
for i, ind in enumerate(mating_pool, start=1):
    print(f"  {i}. '{ind}'")

# ---------- LANGKAH 3: CROSS OVER ----------
print("\n--- Langkah 3: Cross Over (Single Point) ---")
anak = []
for i in range(0, UKURAN_POPULASI, 2):
    p1 = mating_pool[i]
    p2 = mating_pool[(i + 1) % UKURAN_POPULASI]
    a1, a2, titik = crossover_single_point(p1, p2)
    print(f"  Induk1='{p1}' + Induk2='{p2}' | titik potong={titik} "
          f"-> Anak1='{a1}', Anak2='{a2}'")
    anak.extend([a1, a2])
hasil_crossover = anak[:UKURAN_POPULASI]

# ---------- LANGKAH 4: MUTASI ----------
print("\n--- Langkah 4: Mutasi ---")
populasi_baru = []
for ind in hasil_crossover:
    ind_baru, posisi = mutasi(ind, LAJU_MUTASI)
    if posisi:
        detail = ", ".join(f"posisi {p}: '{lama}'->'{baru}'" for p, lama, baru in posisi)
        print(f"  '{ind}' -> '{ind_baru}'  (mutasi: {detail})")
    else:
        print(f"  '{ind}' -> '{ind_baru}'  (tidak ada mutasi)")
    populasi_baru.append(ind_baru)

# ---------- LANGKAH 5: GENERASI BARU ----------
print("\n--- Langkah 5: Generasi Baru (Generasi ke-2) ---")
fitness_baru = evaluasi_populasi(populasi_baru, TARGET)
for i, (ind, f) in enumerate(zip(populasi_baru, fitness_baru), start=1):
    print(f"  Individu {i}: '{ind}'  fitness={f}/{len(TARGET)}")

terbaik_idx = fitness_baru.index(max(fitness_baru))
print(f"\nIndividu terbaik generasi ke-2: '{populasi_baru[terbaik_idx]}' "
      f"(fitness={fitness_baru[terbaik_idx]}/{len(TARGET)})")

if TARGET in KAMUS_SUNDA:
    print(f"\nCatatan: kata '{TARGET}' ada di kamus, artinya = '{KAMUS_SUNDA[TARGET]}'")
