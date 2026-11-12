import json, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

kb = json.load(open("kb.json", encoding="utf-8"))
aturan = kb["aturan"]

# Pertanyaan = syarat yang tidak pernah menjadi hasil aturan
hasil = [r["maka"] for r in aturan]
pertanyaan = []
for r in aturan:
    for f in r["jika"]:
        if f not in hasil and f not in pertanyaan:
            pertanyaan.append(f)

print(kb["judul"])
print("Jawab y/t.")
memori = []
for i, f in enumerate(pertanyaan, 1):
    if input(f"{i}. Apakah {f}? (y/t) > ").strip().lower() == "y":
        memori.append(f)
print("\nFakta awal:", ", ".join(memori) or "(tidak ada)", "\n")

# Forward chaining: ulangi sampai tidak ada aturan baru
asal = {}  # fakta hasil -> aturan yang menghasilkannya
while True:
    cocok = [r for r in aturan
             if r["maka"] not in memori and all(f in memori for f in r["jika"])]
    if not cocok:
        print("Tidak ada aturan baru, berhenti.")
        break
    r = cocok[0]
    memori.append(r["maka"])
    asal[r["maka"]] = r
    print(f"{r['id']}: {' + '.join(r['jika'])} -> {r['maka']}")

# Kesimpulan = hasil yang tidak dipakai aturan lain (kalau tidak ada, tampilkan semua hasil)
dipakai = {f for r in aturan for f in r["jika"]}
akhir = [k for k in asal if k not in dipakai] or list(asal)

def alasan(fakta, tab=1):
    if fakta in asal:
        r = asal[fakta]
        print("  " * tab + f"{fakta} <- {r['id']} ({', '.join(r['jika'])}) [{r['sumber']}]")
        for f in r["jika"]:
            alasan(f, tab + 1)

print("\nKesimpulan:", "; ".join(akhir) if akhir else "tidak ada")
if akhir:
    print("Alasan:")
    for k in akhir:
        alasan(k)
print("\nCatatan:", kb["batas"])