"""
=================================================================
 IMPLEMENTASI ALGORITMA GENETIKA (GENETIC ALGORITHM)
 UNTUK PENCARIAN KATA DALAM KAMUS BAHASA DAERAH SUNDA
=================================================================
 Tugas Mata Kuliah Kecerdasan Buatan
 Bahasa Daerah   : Sunda (Basa Sunda Halus)
 Jumlah Data     : 15 kata (kamus Sunda Halus - Indonesia)
=================================================================

Konsep GA yang diimplementasikan:
- Kromosom / Individu : untai (string) karakter yang panjangnya sama
                        dengan kata target yang dicari.
- Populasi            : sekumpulan kromosom acak.
- Fitness             : jumlah karakter yang cocok (posisi sama)
                        antara individu dan kata target.
- Seleksi             : Roulette Wheel Selection (seleksi roda roulette)
                        berdasarkan probabilitas fitness.
- Crossover           : Single Point Crossover.
- Mutasi              : mutasi acak pada gen (karakter) dengan
                        probabilitas tertentu.
- Generasi Baru       : populasi hasil crossover + mutasi
                        menggantikan populasi lama.
"""

import random
import string

# -----------------------------------------------------------------------
# 1. DATASET KAMUS BAHASA SUNDA HALUS (minimal 10 data kata, di sini 15 data)
# -----------------------------------------------------------------------
KAMUS_SUNDA = {
    "bumi":     "rumah",
    "tuang":    "makan",
    "nginum":   "minum",
    "tilem":    "tidur",
    "tindak":   "pergi",
    "sumping":  "datang",
    "linggih":  "duduk",
    "nangtung": "berdiri",
    "mios":     "keluar",
    "lebet":    "masuk",
    "ningali":  "melihat",
    "ngadangu": "mendengar",
    "nyarios":  "berbicara",
    "neda":     "memohon",
    "wangsul":  "pulang",
}

# -----------------------------------------------------------------------
# Parameter Algoritma Genetika
# -----------------------------------------------------------------------
ALPHABET = string.ascii_lowercase + " "
UKURAN_POPULASI = 8
LAJU_MUTASI = 0.1          # probabilitas mutasi tiap gen
MAKS_GENERASI = 200

# -----------------------------------------------------------------------
# State global (dipakai supaya menu 4-9 bisa dijalankan langkah-per-langkah)
# -----------------------------------------------------------------------
state = {
    "target": None,          # kata yang sedang dicari
    "populasi": [],          # populasi kromosom saat ini
    "fitness": [],           # nilai fitness populasi saat ini
    "mating_pool": [],       # hasil seleksi roulette
    "hasil_crossover": [],   # hasil crossover
    "hasil_mutasi": [],      # hasil mutasi (calon generasi baru)
    "generasi": 0,
}


# =========================================================================
# FUNGSI-FUNGSI INTI ALGORITMA GENETIKA
# =========================================================================
def buat_individu(panjang):
    """Membuat satu kromosom acak sepanjang `panjang` karakter."""
    return "".join(random.choice(ALPHABET) for _ in range(panjang))


def buat_populasi_awal(target):
    """Inisialisasi populasi acak sejumlah UKURAN_POPULASI."""
    panjang = len(target)
    return [buat_individu(panjang) for _ in range(UKURAN_POPULASI)]


def hitung_fitness(individu, target):
    """
    Fitness = jumlah karakter yang sama posisi antara individu & target.
    Semakin besar nilai fitness, semakin mirip individu dengan target.
    Nilai maksimum fitness = panjang(target).
    """
    return sum(1 for a, b in zip(individu, target) if a == b)


def evaluasi_populasi(populasi, target):
    return [hitung_fitness(ind, target) for ind in populasi]


def seleksi_roulette(populasi, fitness, jumlah):
    """
    Roulette Wheel Selection:
    - probabilitas individu = (fitness + 1) / total_fitness
      (ditambah 1 agar individu berfitness 0 tetap punya peluang kecil)
    - individu dipilih secara acak berbobot probabilitas tsb.
    """
    bobot = [f + 1 for f in fitness]  # +1 menghindari total = 0
    total = sum(bobot)
    probabilitas = [b / total for b in bobot]

    terpilih = []
    for _ in range(jumlah):
        r = random.random()
        kumulatif = 0.0
        for ind, p in zip(populasi, probabilitas):
            kumulatif += p
            if r <= kumulatif:
                terpilih.append(ind)
                break
        else:
            terpilih.append(populasi[-1])
    return terpilih, probabilitas


def crossover_single_point(induk1, induk2):
    """Single point crossover: potong di satu titik acak, tukar bagian ekor."""
    panjang = len(induk1)
    if panjang < 2:
        return induk1, induk2
    titik = random.randint(1, panjang - 1)
    anak1 = induk1[:titik] + induk2[titik:]
    anak2 = induk2[:titik] + induk1[titik:]
    return anak1, anak2, titik


def mutasi(individu, laju_mutasi=LAJU_MUTASI):
    """Mutasi tiap gen (karakter) dengan probabilitas `laju_mutasi`."""
    hasil = list(individu)
    posisi_mutasi = []
    for i in range(len(hasil)):
        if random.random() < laju_mutasi:
            gen_lama = hasil[i]
            hasil[i] = random.choice(ALPHABET)
            posisi_mutasi.append((i, gen_lama, hasil[i]))
    return "".join(hasil), posisi_mutasi


# =========================================================================
# FUNGSI-FUNGSI MENU (1 - 10)
# =========================================================================
def menu_1_tampilkan_kamus():
    print("\n=== 1. TAMPILKAN KAMUS BAHASA SUNDA HALUS ===")
    print(f"{'No':<4}{'Bahasa Sunda Halus':<22}{'Bahasa Indonesia':<20}")
    print("-" * 46)
    for i, (kata, arti) in enumerate(KAMUS_SUNDA.items(), start=1):
        print(f"{i:<4}{kata.capitalize():<22}{arti.capitalize():<20}")


def menu_2_cari_kata():
    print("\n=== 2. CARI KATA (PENCARIAN LANGSUNG) ===")
    kata = input("Masukkan kata bahasa Sunda yang dicari: ").strip().lower()
    if kata in KAMUS_SUNDA:
        print(f"Ditemukan! '{kata}' artinya '{KAMUS_SUNDA[kata]}'")
    else:
        print(f"Kata '{kata}' tidak ditemukan di kamus. "
              f"Gunakan menu 3 untuk mencarinya dengan Algoritma Genetika.")


def menu_3_jalankan_ga():
    print("\n=== 3. JALANKAN ALGORITMA GENETIKA ===")
    target = input("Masukkan kata target yang ingin ditemukan GA "
                    "(contoh: salah satu kata di kamus): ").strip().lower()
    if any(c not in ALPHABET for c in target):
        print("Kata hanya boleh mengandung huruf a-z dan spasi.")
        return

    state["target"] = target
    state["populasi"] = buat_populasi_awal(target)
    state["generasi"] = 0
    print(f"Kata target : '{target}' (panjang {len(target)} karakter)")
    print(f"Ukuran populasi awal : {UKURAN_POPULASI}")

    ditemukan = False
    for g in range(1, MAKS_GENERASI + 1):
        state["generasi"] = g
        state["fitness"] = evaluasi_populasi(state["populasi"], target)

        terbaik_idx = state["fitness"].index(max(state["fitness"]))
        terbaik = state["populasi"][terbaik_idx]
        terbaik_fit = state["fitness"][terbaik_idx]

        print(f"\n-- Generasi ke-{g} --")
        print(f"Populasi   : {state['populasi']}")
        print(f"Fitness    : {state['fitness']}")
        print(f"Individu terbaik: '{terbaik}' (fitness={terbaik_fit}/{len(target)})")

        if terbaik == target:
            print(f"\n>> Kata target '{target}' BERHASIL ditemukan pada generasi ke-{g}!")
            ditemukan = True
            break

        # Seleksi
        mating_pool, prob = seleksi_roulette(state["populasi"], state["fitness"], UKURAN_POPULASI)
        state["mating_pool"] = mating_pool

        # Crossover berpasangan
        anak = []
        for i in range(0, UKURAN_POPULASI, 2):
            p1 = mating_pool[i]
            p2 = mating_pool[(i + 1) % UKURAN_POPULASI]
            a1, a2, titik = crossover_single_point(p1, p2)
            anak.extend([a1, a2])
        state["hasil_crossover"] = anak[:UKURAN_POPULASI]

        # Mutasi
        populasi_baru = []
        for ind in state["hasil_crossover"]:
            ind_mutasi, _ = mutasi(ind)
            populasi_baru.append(ind_mutasi)
        state["hasil_mutasi"] = populasi_baru

        # Generasi baru
        state["populasi"] = populasi_baru

    if not ditemukan:
        print(f"\nBatas maksimum {MAKS_GENERASI} generasi tercapai tanpa "
              f"menemukan kecocokan sempurna. Individu terbaik terakhir: "
              f"'{terbaik}' (fitness={terbaik_fit}/{len(target)})")

    if target in KAMUS_SUNDA:
        print(f"Arti kata '{target}' dalam Bahasa Indonesia: {KAMUS_SUNDA[target]}")


def _pastikan_populasi_ada():
    if not state["populasi"]:
        print("Populasi belum ada. Jalankan menu 3 terlebih dahulu, "
              "atau gunakan menu ini untuk membuat populasi awal secara manual.")
        target = input("Masukkan kata target: ").strip().lower()
        state["target"] = target
        state["populasi"] = buat_populasi_awal(target)
        state["generasi"] = 1
    return state["target"]


def menu_4_tampilkan_populasi():
    print("\n=== 4. TAMPILKAN POPULASI ===")
    target = _pastikan_populasi_ada()
    print(f"Generasi ke- : {state['generasi']}")
    print(f"Kata target  : '{target}'")
    for i, ind in enumerate(state["populasi"], start=1):
        print(f"  Individu {i}: '{ind}'")


def menu_5_hasil_fitness():
    print("\n=== 5. HASIL FITNESS ===")
    target = _pastikan_populasi_ada()
    state["fitness"] = evaluasi_populasi(state["populasi"], target)
    for i, (ind, f) in enumerate(zip(state["populasi"], state["fitness"]), start=1):
        print(f"  Individu {i}: '{ind}'  -> fitness = {f}/{len(target)}")


def menu_6_seleksi_roulette():
    print("\n=== 6. SELEKSI ROULETTE ===")
    target = _pastikan_populasi_ada()
    if not state["fitness"]:
        state["fitness"] = evaluasi_populasi(state["populasi"], target)
    mating_pool, prob = seleksi_roulette(state["populasi"], state["fitness"], UKURAN_POPULASI)
    state["mating_pool"] = mating_pool
    print("Probabilitas seleksi tiap individu (berdasar fitness+1):")
    for ind, p in zip(state["populasi"], prob):
        print(f"  '{ind}' -> peluang terpilih = {p:.3f}")
    print("\nMating pool (hasil seleksi roulette):")
    for i, ind in enumerate(mating_pool, start=1):
        print(f"  {i}. '{ind}'")


def menu_7_cross_over():
    print("\n=== 7. CROSS OVER ===")
    if not state["mating_pool"]:
        print("Mating pool belum ada, menjalankan seleksi roulette dahulu...")
        menu_6_seleksi_roulette()
    anak = []
    for i in range(0, len(state["mating_pool"]), 2):
        p1 = state["mating_pool"][i]
        p2 = state["mating_pool"][(i + 1) % len(state["mating_pool"])]
        a1, a2, titik = crossover_single_point(p1, p2)
        print(f"  Induk1='{p1}' + Induk2='{p2}' | titik potong={titik} "
              f"-> Anak1='{a1}', Anak2='{a2}'")
        anak.extend([a1, a2])
    state["hasil_crossover"] = anak[:UKURAN_POPULASI]
    print(f"\nHasil crossover: {state['hasil_crossover']}")


def menu_8_mutasi():
    print("\n=== 8. MUTASI ===")
    if not state["hasil_crossover"]:
        print("Belum ada hasil crossover, menjalankan crossover dahulu...")
        menu_7_cross_over()
    hasil = []
    for ind in state["hasil_crossover"]:
        ind_baru, posisi = mutasi(ind)
        if posisi:
            detail = ", ".join(f"posisi {p}: '{lama}'->'{baru}'" for p, lama, baru in posisi)
            print(f"  '{ind}' -> '{ind_baru}'  (mutasi: {detail})")
        else:
            print(f"  '{ind}' -> '{ind_baru}'  (tidak ada mutasi)")
        hasil.append(ind_baru)
    state["hasil_mutasi"] = hasil
    print(f"\nHasil mutasi (calon generasi baru): {state['hasil_mutasi']}")


def menu_9_generasi_baru():
    print("\n=== 9. GENERASI BARU ===")
    if not state["hasil_mutasi"]:
        print("Belum ada hasil mutasi, menjalankan mutasi dahulu...")
        menu_8_mutasi()
    state["populasi"] = state["hasil_mutasi"]
    state["generasi"] += 1
    state["mating_pool"] = []
    state["hasil_crossover"] = []
    state["hasil_mutasi"] = []
    state["fitness"] = evaluasi_populasi(state["populasi"], state["target"])
    print(f"Populasi diperbarui menjadi generasi ke-{state['generasi']}:")
    for i, (ind, f) in enumerate(zip(state["populasi"], state["fitness"]), start=1):
        print(f"  Individu {i}: '{ind}'  fitness={f}/{len(state['target'])}")


def tampilkan_menu():
    print("\n" + "=" * 55)
    print("   KAMUS BAHASA SUNDA - ALGORITMA GENETIKA")
    print("=" * 55)
    print("1. Tampilkan Kamus")
    print("2. Cari Kata")
    print("3. Jalankan Algoritma Genetika")
    print("4. Tampilkan Populasi")
    print("5. Hasil Fitness")
    print("6. Seleksi Roulette")
    print("7. Cross Over")
    print("8. Mutasi")
    print("9. Generasi Baru")
    print("10. Keluar")


def main():
    aksi = {
        "1": menu_1_tampilkan_kamus,
        "2": menu_2_cari_kata,
        "3": menu_3_jalankan_ga,
        "4": menu_4_tampilkan_populasi,
        "5": menu_5_hasil_fitness,
        "6": menu_6_seleksi_roulette,
        "7": menu_7_cross_over,
        "8": menu_8_mutasi,
        "9": menu_9_generasi_baru,
    }
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-10): ").strip()
        if pilihan == "10":
            print("Keluar dari program. Hatur nuhun!")
            break
        fungsi = aksi.get(pilihan)
        if fungsi:
            fungsi()
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()
