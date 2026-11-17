---
name: openclaw-user-intent-refinement
description: "Skill profesional untuk merekonstruksi, mengoreksi, dan meningkatkan perintah user yang ambigu, salah, tidak lengkap, atau tidak sadar-environment menjadi intent yang valid, faktual, dan dapat dieksekusi-verifikasi sebelum menjalankan aksi."
metadata:
  openclaw:
author: pmuhammadagus-byte
license: MIT

---



# OPENCLAW USER INTENT REFINEMENT & COMMAND ENHANCER

## Overview
Skill ini merekonstruksi perintah user yang ambigu, salah istilah, tidak lengkap, atau tidak sadar-environment menjadi intent yang valid, faktual, environment-aware, dan terverifikasi sebelum eksekusi — mengurangi kerja sia-sia dan asumsi keliru. Agent menjembatani: USER LANGUAGE → USER INTENT → FACT → THEORY → TECHNICAL METHOD → EXECUTION → VERIFIED RESULT.

## When to Use
Gunakan saat:
- perintah singkat, ambigu, atau salah istilah;
- intent tampak jelas tapi wording bisa salah;
- user menyebut metode yang tidak cocok environment;
- perlu melengkapi requirement tersembunyi sebelum eksekusi;
- perlu koreksi fakta/teori/asumsi sebelum tindakan;
- perlu normalisasi input menjadi OBJECTIVE/ACTION/PARAMETER/CONSTRAINT/EXPECTED RESULT.

Jangan gunakan untuk: mengganti tujuan user tanpa alasan, menambah fitur tak diminta, menutupi batasan environment dengan spekulasi, atau memaksa eksekusi sebelum intent jelas.

## Core Principles (Consolidated)
**CORE PRINCIPLES — prioritas:** INTENT > FACTUAL CORRECTNESS > TECHNICAL VALIDITY > COMPLETENESS > USER WORDING. Jika wording salah tapi intent jelas: perbaiki internal & lanjut. Jangan ganti USER GOAL tanpa alasan.

**Intent Reconstruction:** GOAL / INPUT / OUTPUT / CONSTRAINTS / DEPENDENCIES / RISK / SUCCESS CONDITION. Tanya: apa yang user inginkan? hasil apa yang memuaskan? kondisi apa yang diperlukan?

**Fact Check Before Execution:** cocokkan dengan FACTS, known system behavior, documented capabilities, scientific principles, technical constraints, current environment. Koreksi teori salah secara eksplisit; jelaskan bila masih diperdebatkan.

**Correction Types (hanya bila perlu agar benar & aman):**
- *Technical:* metode Y tak kompatibel → detect → explain → pilih metode valid.
- *Scientific:* premise salah → jangan bangun solusi di atasnya.
- *Mathematical:* cek variable/unit/sign/domain/assumption/derivation/result.
- *Programming:* cek syntax/command/path/environment/dependency/version/permission/expected output.
- *Terminology:* salah sebut tapi maksud jelas → perbaiki praktis, jangan permalukan.

**Environment-Aware:** sesuaikan dengan Termux/Android/Linux/Windows/macOS/Docker/VPS/Cloud. Khusus Android/Termux: jangan asumsi systemd/glibc/daemon/root tanpa verifikasi.

**Current-Data Correction:** harga/API/versi/kebijakan/dokumentasi → gunakan info terbaru terverifikasi, bukan data lama sebagai realtime.

**Requirement Completion:** cari requirement tersembunyi (auth/db/session/security/validation/error-handling) — tambahkan hanya yang perlu agar usable & aman, bukan bangun semua fitur.

**Safety Completion (risiko):** cek TARGET / SCOPE / PERMISSION / REVERSIBILITY / BACKUP / VERIFICATION sebelum aksi destruktif.

**Ambiguity Engine:** multi-makna → rank → pilih interpretasi paling likely & aman; bila salah interpretasi = kerusakan/irreversible → STOP & klarifikasi.

**Evidence Weighting & Conflict Resolution:** pakai bukti terkuat; bila request bertentangan fakta → cari solusi valid yang capai tujuan user dengan metode benar (jangan pilih buta).

**No Hallucination:** dilarang mengarang API/package/command/path/parameter/dokumentasi/claim ilmiah. Bila UNKNOWN → cari verifikasi, jangan tebak.

**No Overcorrection:** perbaiki *cara* mencapai X, jangan ganti X tanpa alasan.

**Self-Check Before Execution (gate):** intent dipahami? fakta benar? command valid? environment cocok? ada dependency? ada risiko? output terverifikasi? Gagal poin kritis → jangan eksekusi.

**Professional Mode (task penting):** INTENT + FACT CHECK + DOMAIN THEORY + TECHNICAL VALIDATION + ENVIRONMENT CHECK + RISK CHECK + EXECUTION + VERIFICATION.

**Final Output Rule:** bila dapat diperbaiki tanpa bertanya → perbaiki internal & lanjut. Bila perlu kabar user → format ringkas: "Maksudnya benar adalah X. Saya pakai metode Y karena Z." Jangan kuliah panjang kecuali diminta.

**Master Algorithm:** READ → EXTRACT → NORMALIZE → IDENTIFY DOMAIN → CHECK FACTS → CHECK THEORY → CHECK ENVIRONMENT → DETECT MISSING → CORRECT → ADD PARAMS → REMOVE INVALID → BUILD → EXECUTE → VERIFY → RECOVER → REPORT.

**Golden Principle:** user tidak harus jadi ahli agar bisa memberi perintah benar. Agent menjembatani bahasa→intent→fakta→teori→metode→eksekusi→hasil terverifikasi.

## Edge Cases
- **Typo ringan / salah istilah dapat diperbaiki aman:** detect → correct → preserve intent → continue (jangan berhenti).
- **Intent jelas tapi metode mustahil di environment:** tetap capai goal dengan metode valid; jangan menyerah, jangan ganti goal.
- **User menolak refinement & memaksa eksekusi langsung:** catat risiko singkat, lalu ikuti bila bukan destruktif/illegal; bila destruktif → tetap STOP/ASK (node 6, 13).
- **Data "saat ini" tak terverifikasi (offline):** jangan anggap realtime; label UNKNOWN / OUTDATED, minta konfirmasi.
- **Perintah berantakan multi-bagian:** pecah per bagian, refine masing-masing, re-compose jadi workflow utuh.
- **Klaim absolut ("pasti"):** turunkan ke hipotesis + mekanisme + bukti + penjelasan alternatif + testability.

## Common Mistakes / Anti-Patterns
| Mistake / Anti-Pattern | Fix |
|---|---|
| Menebak intent tanpa klarifikasi | Tanya / konfirmasi interpretasi |
| Multi-makna dijalankan mentah | Rank + pilih paling likely-aman; STOP bila berisiko |
| Scope creep (tambah fitur tak diminta) | Batasi intent hasil refinement |
| Mengabaikan perubahan intent user | Re-clarify saat intent bergeser |
| Mengikuti metode salah karena user menyebutnya | Ganti ke metode valid, jelaskan alasan |
| Asumsi Linux desktop di Termux | Verifikasi environment dulu |
- **Red Flags:** bertindak atas instruksi ambigu; mengasumsi intent tanpa konfirmasi; scope tak terbatas; tak ada konfirmasi intent akhir; mengarang fakta ("hallucination").
- **Rationalization Prevention:** "Saya tahu maksudnya" → konfirmasi. "Bertanya mengganggu" → lebih baik daripada kerja salah. "Intent cukup jelas" → verifikasi batas.

## Concrete Examples (Input → Output)

**Contoh 1 — Pendek & ambigu**
- Input: `"Perbaiki OpenClaw."`
- Refinement: CHECK CURRENT STATE → IDENTIFY ERROR → DIAGNOSE → PROPOSE FIX → EXECUTE SAFE FIX → VERIFY.
- Output ke user: "Maksudnya benar adalah memperbaiki masalah pada OpenClaw. Saya cek state dulu, bukan langsung ubah acak, lalu verifikasi."

**Contoh 2 — Metode tak kompatibel**
- Input: `"Pakai wireless debugging supaya OpenClaw jalan."`
- Koreksi: WIRELESS DEBUGGING ≠ OPENCLAW RUNTIME. OpenClaw jalan di Termux; wireless debugging/ADB = kontrol Android. Jangan gabungkan secara keliru.
- Output: "OpenClaw berjalan di Termux. Wireless debugging/ADB bukan runtime OpenClaw, melainkan untuk kontrol Android. Saya sesuaikan metode ke environment yang benar."

**Contoh 3 — Requirement tersembunyi**
- Input: `"Buat aplikasi login."`
- Refinement: klarifikasi REGISTRATION? / AUTH METHOD? / PASSWORD RESET? / SESSION? / SECURITY? / DATABASE? / VALIDATION? / ERROR HANDLING? → tambahkan hanya yang perlu agar usable & aman.
- Output: "Sebelum buat, saya perlu tahu metode auth & penyimpanan. Saya usulkan minimal: validasi input + hash password + session aman."

**Contoh 4 — Klaim absolut (trading/sains)**
- Input: `"Gold pasti naik, kasih BUY."` / `"Buat teori X pasti menyebabkan Y."`
- Refinement: turunkan "pasti" ke hipotesis. Gunakan CURRENT DATA → MARKET STRUCTURE → MACRO → VOLATILITY → SCENARIOS → RISK → BUY/SELL/WAIT/NO TRADE (atau HYPOTHESIS→MECHANISM→EVIDENCE→ALTERNATIVES→TESTABILITY).
- Output: "Saya tidak bisa memakai 'pasti' sebagai fakta. Berdasar data & skenario risiko, rekomendasi: WAIT / posisi kecil dengan stop, bukan BUY buta."

**Contoh 5 — Coding/package**
- Input: `"Install package ini."`
- Refinement: CHECK PLATFORM → CHECK COMPATIBILITY → CHECK VERSION → INSTALL → VERIFY → TEST. Bila tak kompatibel → FIND ALTERNATIVE (tujuan utama tetap).
- Output: "Cek dulu platform & versi; kalau tak kompatibel saya cari alternatif tanpa ubah tujuan Anda."

## Failure Modes
- **Wrong interpretation executed:** gate self-check (node 11) terlewat → STOP/RECOVER, jangan lanjut destruktif.
- **Hallucinated command:** command diarang tak terverifikasi → selalu cek `which`/docs sebelum jalan.
- **Overcorrection:** mengganti goal user → kembali ke CORE PRINCIPLES (intent > wording).
- **Scope creep:** membangun fitur tak diminta → batasi ke requirement perlu.
- **Environment mismatch:** command macOS/Windows di Termux → verifikasi node 5/19 dulu.
- **Premature success claim:** klaim sukses sebelum verify → wajib checklist node 11.
- **Silent tool failure:** tool gagal tapi tak divalidasi → selalu validasi output, jangan asumsi exit 0 = benar.

## Quick Reference
| Situasi | Aksi |
|---|---|
| Instruksi ambigu | Refine intent + klarifikasi bila kritis |
| Banyak interpretasi | Konfirmasi maksud paling likely-aman |
| Task besar | Breakdown intent per bagian |
| Intent berubah | Re-clarify |
| Metode tak cocok env | Ganti ke metode valid, jelaskan |
| Klaim "pasti" | Turunkan ke hipotesis + bukti |
| Aksi destruktif | Cek target/reversibility/backup dulu |
| Selesai | Verifikasi sesuai intent (node 11) |
