# Tugas 5: Sistem Pakar Sederhana, Penyebab Ikan Hias Stres atau Mati Mendadak di Akuarium

- Nama : **WIRABUANA RAMADHANA JAUHARI**
- NIM  : **F1D02510030**

## Topik dan cara menjalankan
Menentukan kemungkinan penyebab ikan hias stres atau mati mendadak di akuarium, berdasarkan kondisi air dan perawatan.
Bahasa: Python 3 (tanpa library tambahan, mesin inferensi ditulis sendiri).

```bash
python sistem_pakar.py
```
Jawab pertanyaan dengan `y` atau `t`. File aturan: `kb.json` (harus satu folder dengan program).

## Sumber
| Kode | Sumber |
|---|---|
| S1 | Wigati, L., Susilowati, T., Amalia, R. (2023). *Pengaruh Persentase Pergantian Air terhadap Pertumbuhan dan Kelulushidupan Ikan Rainbow (Melanotaenia boesmani)*. Jurnal Sains Akuakultur Tropis 7(1): 39-44, Universitas Diponegoro. https://ejournal2.undip.ac.id/index.php/sat/article/download/12638/pdf. Diakses 12 Nov 2026. |
| S2 | Wahyudi, Setiyono, A., Jayanthi, O.W. (2014). *Studi Kualitas dan Potensi Pemanfaatan Airtanah Dangkal di Pesisir Surabaya Timur*. Eksplorium 35(1): 43-56, BATAN. https://jurnal.batan.go.id/index.php/eksplorium/article/download/1837/1735. Diakses 12 Nov 2026. |

Catatan sumber: S1 meneliti ikan hias rainbow. S2 membahas air tanah, tetapi bagian toksisitas amonia dan nitrit pada ikan merujuk ke OATA (2008), asosiasi perdagangan ikan hias.

## Tabel aturan
| Aturan | IF | THEN | Sumber |
|---|---|---|---|
| R1 | kotoran dan sisa pakan menumpuk di dasar akuarium | amonia tinggi | S2 |
| R2 | hasil tes amonia (NH3) di atas 0,2 mg/L | amonia tinggi | S2 |
| R3 | amonia tinggi | **keracunan amonia** (iritasi dan kerusakan insang) | S1, S2 |
| R4 | hasil tes nitrit di atas 0,06 mg/L | **keracunan nitrit** (darah sulit mengangkut oksigen) | S2 |
| R5 | pH atau suhu air di luar kisaran yang cocok untuk jenis ikan | **stres karena lingkungan tidak sesuai** | S1 |
| R6 | amonia tinggi AND air jarang diganti dan dasar akuarium jarang disipon | **risiko kematian tinggi** | S1 |

6 aturan, 4 kesimpulan akhir (cetak tebal). Aturan berantai: R1 -> R3 dan R1 -> R6 (juga R2 -> R3 dan R2 -> R6).

Dasar angka: amonia bebas (NH3) di atas 0,2 mg/L membuat ikan stres dan pada kadar lebih tinggi merusak insang hingga mati (S2); nitrit di atas 0,06 mg/L melewati batas untuk perikanan (S2). Pada penelitian S1, akuarium tanpa pergantian air memiliki kelulushidupan terendah (44%) dan amonia tertinggi.

## Metode: Forward Chaining
Dipilih karena fakta akuarium (kondisi air, hasil tes, kebiasaan perawatan) sudah diketahui lebih dulu, lalu dicari kesimpulannya.
1. Fakta yang dijawab "ya" masuk ke memori.
2. Cari aturan yang semua syaratnya ada di memori dan hasilnya belum ada di memori.
3. Jika ada, tambahkan hasilnya ke memori dan ulangi. Jika tidak ada, berhenti.
4. Alasan ditelusuri mundur dari kesimpulan lewat aturan yang menghasilkannya.

Jika R1 dan R2 sama-sama terpenuhi, hanya R1 yang dicatat sebagai alasan karena "amonia tinggi" sudah ada di memori.

## Kasus uji
Urutan pertanyaan: (1) kotoran/sisa pakan menumpuk, (2) tes amonia > 0,2, (3) tes nitrit > 0,06, (4) pH/suhu di luar kisaran, (5) air jarang diganti.

| # | Jawaban | Kesimpulan |
|---|---|---|
| 1 | `y t t t y` (kotoran menumpuk, jarang ganti air) | keracunan amonia; risiko kematian tinggi |
| 2 | `t t t t t` (semua tidak) | **tidak ada** (kasus negatif) |
| 3 | `t t y y t` (nitrit tinggi, pH/suhu tidak cocok) | keracunan nitrit; stres karena lingkungan tidak sesuai |
| 4 | `t y t t y` (tes amonia tinggi, jarang ganti air) | keracunan amonia; risiko kematian tinggi |

Keluaran asli kasus 1:

```
Fakta awal: kotoran dan sisa pakan menumpuk di dasar akuarium, air jarang diganti dan dasar akuarium jarang disipon

R1: kotoran dan sisa pakan menumpuk di dasar akuarium -> amonia tinggi
R3: amonia tinggi -> keracunan amonia (iritasi dan kerusakan insang)
R6: amonia tinggi + air jarang diganti dan dasar akuarium jarang disipon -> risiko kematian tinggi
Tidak ada aturan baru, berhenti.

Kesimpulan: keracunan amonia (iritasi dan kerusakan insang); risiko kematian tinggi
Alasan:
  keracunan amonia (iritasi dan kerusakan insang) <- R3 (amonia tinggi) [S1, S2]
    amonia tinggi <- R1 (kotoran dan sisa pakan menumpuk di dasar akuarium) [S2]
  risiko kematian tinggi <- R6 (amonia tinggi, air jarang diganti dan dasar akuarium jarang disipon) [S1]
    amonia tinggi <- R1 (kotoran dan sisa pakan menumpuk di dasar akuarium) [S2]
```

## Batas keberlakuan
Pengetahuan berasal dari dua publikasi akademik, bukan pengalaman penghobi ikan. Aturan hanya mencakup amonia, nitrit, pH/suhu, dan frekuensi ganti air. Penyebab lain seperti penyakit, kepadatan ikan, ikan agresif, racun atau bahan kimia, dan listrik mati tidak dicakup. Kisaran pH dan suhu yang cocok berbeda tiap spesies; S1 meneliti ikan rainbow, sehingga pengguna harus mencocokkan dengan jenis ikannya. Hasilnya saran awal, bukan keputusan akhir; untuk kematian massal, konsultasikan dengan penyuluh perikanan atau dokter hewan ikan. Catatan ini juga ditampilkan oleh program.
