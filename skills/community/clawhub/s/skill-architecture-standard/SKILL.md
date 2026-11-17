---
name: skill-architecture-standard
description: "Gunakan sebagai referensi saat user membuat, mereview, atau upgrade skill OpenClaw."
metadata:
  openclaw:
    version: 1.1.2
    applies_to: "new skills authored after 2026-08-25"
---

# SKILL ARCHITECTURE STANDARD X∞

> **Status:** Panduan referensi (recommended). Digunakan saat membuat skill baru. Skill yang mengikuti struktur ini lebih konsisten, tapi tidak wajib.
>
> **Versi:** 1.1.0 — Peningkatan kelas profesional: trigger engine berbasis frasa konkret, tabel keputusan IF→MAKA, runbook eksekusi berurutan, engine verifikasi pasca-aksi nyata, hierarki recovery berjenjang, serta penambahan *Edge Cases*, *Anti-Patterns*, *Concrete Examples*, dan *Failure Modes* di setiap node relevan.

---

## 1. IDENTITY

**Nama:** Skill Architecture Standard X∞

**Peran:** Kerangka arsitektur *recommended* yang berada di atas seluruh skill OpenClaw — baik skill baru maupun skill warisan (*legacy*). Mengikuti standard ini bersifat anjuran, bukan pemaksaan.

**Tanggung jawab:**
- Menetapkan struktur kanonik 21-node yang disarankan untuk setiap skill.
- Menjadi rujukan saat agent **membuat**, **mereview**, atau **meng-upgrade** skill apa pun.
- Menandai (sebagai rekomendasi) setiap skill yang menyimpang dari struktur ini.

**Otoritas:** Dalam cakupan arsitektur skill sebagai rujukan. Agent disarankan memuat standard ini saat membuat/mereview skill. Standard ini tidak menjalankan tugas domain (debug, deploy, dsb) — ia menentukan **bagaimana** skill domain sebaiknya dibangun dan berperilaku.

**Batas kewenangan:** Standard ini tidak mengganti logika domain skill; ia menetapkan *contract* perilaku. Pelanggaran struktur = skill ditolak, bukan dijalankan sebagian.

---

## 2. PURPOSE

Metadata statis tidak cukup untuk menghasilkan skill yang agentik. Skill taraf tinggi harus memenuhi empat kemampuan operasional:

| # | Kemampuan | Kriteria sukses terukur |
|---|-----------|--------------------------|
| 1 | **Tahu kapan aktif** | Mengaktivasi diri dari *intent* user tanpa menyebut nama skill (trigger engine). |
| 2 | **Tahu bagaimana bertindak** | Memiliki *policy* (IF→MAKA), bukan sekadar kumpulan pengetahuan pasif. |
| 3 | **Tahu mengukur diri** | Mengeksekusi verification, evaluation, dan observability setelah bertindak. |
| 4 | **Tahu bereaksi saat berubah** | Punya recovery, fallback, dan exit condition saat kondisi melenceng. |

**Tujuan akhir:** menaikkan seluruh skill ke taraf *agen nyata* — skill yang memutuskan, bertindak, memverifikasi, dan pulih — bukan dokumen pengetahuan yang hanya menunggu dibacakan.

**Anti-pattern yang dicegah:** skill "buku resep" yang hanya menjawab, tidak bertindak, tidak memverifikasi, dan tidak tahu kapan berhenti.

---

## 3. METADATA

Setiap skill WAJIB membawa frontmatter YAML berikut:

```yaml
---
name: <slug-konsisten-tanpa-spasi>
description: "<kalimat trigger-centric: kapan dipakai + kata kunci aktivasi + hasil yang diberikan>"
metadata:
  openclaw:
    version: <semver>
    requires:
      bins: [<binary eksternal jika wajib>]
      env: [<environment variable yang dibutuhkan>]
      os: [<sistem operasi yang didukung>]
---
```

**Aturan ketat:**
1. `description` wajib **trigger-centric**: sebutkan pola kalimat user yang mengaktifkan skill dan hasil yang dijanjikan. Ini bukan ringkasan fitur.
2. `version` mengikuti SemVer (MAJOR.MINOR.PATCH).
3. Jika skill butuh binary eksternal, catatkan di dalam isi skill: cara rebuild, versi yang diuji, dan fallback bila binary absen.
4. `name` konsisten dengan slug direktori; jangan gunakan spasi atau karakter aneh.

**Contoh description yang baik:**
> "Bantu debug error website pasca-deploy. Aktif saat user menyebut 'website error setelah deploy', 'aplikasi 500 setelah rilis', atau 'rollback gagal'. Menyediakan runbook diagnosis + verifikasi."

**Failure mode:** `description` yang hanya berisi "alat untuk X" menyebabkan trigger engine tidak bisa mengenali aktivasi otomatis → skill mati tak terpakai.

---

## 4. TRIGGER ENGINE

Skill harus tahu **kapan harus dipakai** sendiri, tanpa user menyebut nama file.

### 4.1 Pola pemicu spesifik (contoh konkret — sesuaikan per skill)
Gunakan kelas pola berikut, bukan daftar kata kunci longgar:
- **Frasa aksi + domain:** "website saya error setelah deploy", "aplikasi lemot pas peak", "cron gagal tiap jam".
- **Situasi bermasalah:** "sudah coba restart tapi tetap 500", "token expired terus".
- **Permintaan hasil:** "tolong bikin skill untuk X", "review skill ini", "upgrade standar skill".

### 4.2 Contoh kalimat user → aktivasi
| Kalimat user | Taxonomy terdeteksi |
|--------------|---------------------|
| "Web saya 502 setelah push ke prod." | WEB DEBUGGING + DEPLOYMENT + ERROR ANALYSIS |
| "Bikin skill buat format log JSON." | SKILL CREATION + FORMATTING |
| "Review SKILL.md ini, kurang apa?" | SKILL REVIEW + COMPLIANCE |

### 4.3 Taksonomi trigger (kategori)
`WEB`, `DEPLOYMENT`, `DEBUG`, `OBSERVABILITY`, `SKILL CREATION`, `SKILL REVIEW`, `SECURITY`, `PERFORMANCE`, `DATA`, `CONFIG`. Setiap skill mendeklarasikan 1–3 taksonomi utama.

### 4.4 Negative triggers (kapan TIDAK aktif)
- User hanya bertanya definisi/consep umum tanpa niat eksekusi ("apa itu deploy?").
- Skill lain memiliki taksonomi lebih spesifik dan telah aktif (hindari tumpang tindih).
- Permintaan di luar os/arsitektur yang didukung (lihat node 19).

### 4.5 Logika aktivasi
```
TERIMA INPUT
  → COCOK dengan positif trigger?  → AKTIF
  → COCOK dengan negative trigger? → TIDAK AKTIF (serahkan ke skill lain / jawab langsung)
  → AMBIGU → muat context (node 5), lalu PUTUSKAN
```

**Edge case:** input ambigu ("bantu saya") → jangan asumsi aktif; tanyakan klarifikasi singkat atau muat context dulu.

---

## 5. CONTEXT ENGINE

Skill wajib memahami konteks sebelum memberi instruksi atau bertindak. Dimensi konteks:

| Dimensi | Contoh isi |
|---------|-----------|
| USER | tingkat teknis, preferensi bahasa |
| TASK | tujuan spesifik, batas waktu |
| ENVIRONMENT | Termux Android ARM64 vs Ubuntu x86_64 |
| OS / ARCH | Linux 6.x / arm64 |
| TOOLS | binary tersedia atau tidak |
| AVAILABLE SKILLS | skill lain yang relevan & aktif |
| PREVIOUS ACTIONS | langkah sudah diambil |
| CURRENT STATE | status sistem saat ini |
| CONSTRAINTS | izin, kuota, kebijakan |

**Contoh kritis:** Jangan beri instruksi `apt install` atau `systemctl` ketika user berada di **Termux Android ARM64** — gunakan `pkg`/`termux-services`. Instruksi yang salah environment = kegagalan langsung.

**Failure mode:** mengasumsikan environment desktop Linux → perintah gagal, user kehilangan kepercayaan.

**Aturan:** Baca konteks (termasuk `session_status`/`uname -a` bila relevan) **sebelum** bertindak, bukan sesudahnya.

---

## 6. DECISION POLICY

Ini pembeda skill pasif vs skill agentik. Wajib berisi tabel **KONDISI → MAKA + ALASAN**.

| IF / KONDISI | MAKA | ALASAN |
|--------------|------|--------|
| Kondisi cocok trigger positif | AKTIF & jalankan runbook | Hindari inaktivitas skill |
| Ketidakpastian tinggi | VERIFIK / Klarifikasi | Cegah asumsi berbahaya |
| Risiko TINGGI/CRITICAL | ASK / STOP + minta approval | Lindungi sistem user |
| Tool wajib tidak tersedia | PAKAI alternatif / beri tahu | Jangan gagal diam-diam |
| Aksi gagal | RECOVER (node 12) | Pulih, jangan menyerah |
| Sudah capai exit condition | BERHENTI & laporkan | Cegah loop tak berujung |
| Instruksi bertentangan dengan guardrail | TOLAK + jelaskan | Keamanan > kenyamanan |

**Klasifikasi risiko (standar):**
```
READ FILE         → LOW
INSTALL PACKAGE   → MEDIUM
MODIFY CONFIG     → MEDIUM
DELETE / DROP     → CRITICAL
```
Semakin tinggi risiko → verifikasi (node 11) dan approval (node 13) semakin ketat.

**Anti-pattern:** skill yang hanya berisi "lakukan X" tanpa cabang keputusan untuk kondisi gagal/ambiguitas.

---

## 7. REASONING POLICY

**Siklus berpikir wajib:**
```
BELAJAR (kumpulkan fakta)
  → PAHAMI (bedakan fakta vs hipotesis)
  → RENCANAKAN (langkah + tool)
  → BERTINDAK (eksekusi)
  → PERIKSA (verifikasi)
  → PERBAIKI (recovery bila perlu)
  → SELESAI (exit condition)
```

**Prinsip:**
- **Evidence-first:** jangan mengarang hipotesis sebelum data ada. Cari bukti dulu.
- **Fakta vs Hipotesis:** labeli secara eksplisit dalam penalaran internal.
- **Confidence scale:** `CONFIRMED` / `LIKELY` / `POSSIBLE` / `UNKNOWN`. Jangan gunakan `CONFIRMED` tanpa bukti.

**Common mistake:** melompat ke kesimpulan (`CONFIRMED`) dari gejala tunggal tanpa korelasi → diagnosis salah.

---

## 8. EXECUTION POLICY

**Runbook eksekusi berurutan (template):**
1. **Validasi context** (node 5) — pastikan environment & izin sesuai.
2. **Tentukan langkah** berdasar decision policy (node 6).
3. **Pilih tool** sesuai tool policy (node 9).
4. **Eksekusi** tindakan secara atomik bila memungkinkan.
5. **VERIFIKASI** hasil (node 11) — jangan klaim sukses sebelum terbukti.
6. **Laporkan** hasil + bukti ke user.
7. **Cek exit condition** (node 21) — berhenti bila terpenuhi.

**Preferensi tool (urut prioritas):**
- Baca/ubah file lokal → tool `read`/`write`/`edit`, bukan membuka web.
- Info eksternal terkini → `web_fetch`/`web_search`, bukan menebak.
- Operasi sistem → `exec`, dengan penggunaan `trash` bukan `rm` saat memungkinkan.

**Anti-pattern:** menjawab dengan teks panjang tanpa mengambil tindakan saat tugas jelas membutuhkan aksi (mis. user minta "perbaiki file ini").

**Aturan emas:** **Jangan klaim sukses sebelum diverifikasi.**

---

## 9. TOOL POLICY

| Tool | GUNAKAN KETIKA | JANGAN GUNAKAN KETIKA |
|------|----------------|------------------------|
| SEARCH (`web_search`) | Info hilang / butuh sumber terkini | Fakta sudah ada di context lokal |
| FILES (`read`/`write`/`edit`) | Dokumen/code lokal | Ingin mengubah sistem eksternal |
| GITHUB | Operasi repository | Tidak ada repo terkait |
| WEB (`web_fetch`) | Ambil konten URL spesifik | Cukup baca file lokal |
| TERMINAL (`exec`) | Operasi sistem/proses | Tugas murni pengetahuan |

**Algoritma pemilihan:**
```
BUTUH DATA?
  → lokal ada?      → FILES
  → eksternal?      → WEB / SEARCH
BUTUH AKSI SISTEM?  → TERMINAL
JANGAN panggil semua tool sekaligus — pilih berdasar kebutuhan + context.
```

**Edge case:** tool gagal (timeout/permission) → lihat node 12, jangan lanjut asumsi sukses.

---

## 10. MEMORY POLICY

| Aspek | Kebijakan |
|-------|-----------|
| **WHAT** to remember | Keputusan, preferensi user, konteks tugas, pelajaran (*lessons learned*) |
| **WHAT NOT** | Noise, log mentah, rahasia, data sesi sekali pakai |
| **WHEN** retrieve | Saat context relevan & usia masuk akal |
| **WHEN** update | Setelah tindakan terverifikasi & bernilai jangka panjang |
| **WHEN** ignore | Memory usang/bertentangan dengan state saat ini |

**Tujuan:** mencegah memory menjadi sampah (*memory bloat*). Simpan esensi, bukan log harian mentah.

**Anti-pattern:** menulis ulang memory dengan placeholder kosong ("akan diisi nanti") — itu bukan memori, itu noise.

---

## 11. VERIFICATION ENGINE

Verifikasi bukan sekadar mengecek *exit code 0*. **Bukti harus sesuai jenis aksi.**

### 11.1 Checklist verifikasi pasca-aksi
- [ ] **State berubah sesuai harapan?** (bukan cuma "perintah selesai")
- [ ] **Efek samping tidak merusak?** (file lain, config, layanan)
- [ ] **Output dapat dibuktikan?** (baca balikan, cek hash, cek status)
- [ ] **Risiko tinggi → approval tercatat?** (node 13)
- [ ] **User dapat mengonfirmasi?** (beri cara cek mandiri)

### 11.2 Metode verifikasi per jenis aksi
| Aksi | Cara verifikasi nyata |
|------|------------------------|
| Tulis/edit file | `read` ulang bagian yang diubah, pastikan diff sesuai |
| Install package | jalankan `<bin> --version` / cek keberadaan binary |
| Modify config | muat ulang/validasi config (`nginx -t`, `systemctl status`) |
| Deploy | cek endpoint / log / health check |
| Delete | pastikan target benar-benar hilang & tidak ada dependency rusak |

**Contoh konkret (input→output):**
```
INPUT : user "hapus baris X di config nginx"
EKSEKUSI: edit config
VERIFIKASI: `nginx -t` → "syntax is ok" + `read` config → baris X tidak ada
OUTPUT: "Berhasil. nginx -t valid, baris X terhapus. (bukti: ...)"
```

**Failure mode:** klaim "sukses" karena `exit 0` padahal file tidak berubah (permission silent fail).

---

## 12. ERROR RECOVERY

### 12.1 Hierarki recovery berjenjang
```
ERROR
├── transient (jaringan/sempoyongan) → RETRY (max 3, exponential backoff)
├── timeout                     → BACKOFF + cek resource, lalu retry/alternatif
├── auth                        → CEK kredensial, minta user perbarui (jangan log)
├── dependency missing          → DIAGNOSA dependency, pasang/alternatif
├── permission denied           → DIAGNOSA izin, minta approval (node 13)
├── unsupported (os/arch)       → GUNAKAN alternatif kompatibel (node 19)
└── unknown                     → INVESTIGATE (kumpulkan log), lalu PUTUSKAN/ASK
```

### 12.2 Runbook recovery
1. **Klasifikasi** error ke hierarki di atas.
2. **Terapkan** tindakan recovery lapis pertama.
3. **Verifikasi** (node 11) apakah pulih.
4. Bila gagal di semua lapis → **ESKALASI**: beri tahu user + berikan diagnosis, jangan loop.

**Contoh:** `exec` gagal `permission denied` saat `systemctl` → cek apakah di Termux (tidak ada systemd) → gunakan `termux-services` sebagai alternatif, atau minta approval `elevated`.

**Anti-pattern:** retry tanpa batas (hang/loop) atau menyerah tanpa diagnosis.

---

## 13. SECURITY GUARDRAILS

**WAJIB:**
- **NEVER** log secret, API key, token, password.
- **NEVER** expose kredensial ke output user atau file memory.
- **REDACT** sebelum menyimpan: `API KEY / TOKEN / PASSWORD / SECRET / PRIVATE KEY / COOKIE / SESSION / AUTHORIZATION / BEARER` → `[REDACTED]`.
- **PII:** MINIMIZE (jangan kumpulkan) → REDACT (jika muncul) → HASH (jika wajib disimpan).
- **FAIL-SAFE:** jika observability gagal, agent **tetap jalan** (kecuali requirement keamanan eksplisit melarang).

**Edge case:** token muncul di log tak terduga → redact seketika, jangan teruskan ke memory/output.

**Hard rule:** tidak ada PII (email pribadi, URL repo pribadi, token) yang ditulis ke dalam file skill.

---

## 14. EVALUATION

Setelah selesai, skill menjalankan self-evaluation:

| Pertanyaan | Tindak lanjut bila "TIDAK" |
|------------|----------------------------|
| Capai tujuan user? | Kembali ke decision policy |
| Hasil terverifikasi? | Jalankan verification engine |
| Ada asumsi tak terkonfirmasi? | Labeli UNKNOWN / klarifikasi |
| Ada yang gagal? | Catat di failure modes + recovery |

**Skor kualitas (opsional):** `GOAL_MET`, `VERIFIED`, `ASSUMPTIONS_MINIMIZED`, `FAILURES_HANDLED` → kirim ke Agent Evaluation Engine untuk regresi/benchmark.

**Common mistake:** melaporkan "selesai" tanpa mengevaluasi asumsi → bug terbawa.

---

## 15. OBSERVABILITY

Skill emit signal ke Observability & Trace Engine:

| Signal | Kapan |
|--------|-------|
| START | awal eksekusi |
| PROGRESS | tiap tahap runbook |
| TOOL CALL | sebelum/selesai panggil tool |
| ERROR | saat error terdeteksi |
| RETRY | saat recovery dijalankan |
| SUCCESS | exit sukses |
| FAILURE | exit gagal |

Setiap signal menyertakan: `TRACE_ID`, `SPAN`, `STATUS`, `DURATION` — **tanpa secret**.

**Edge case:** trace engine offline → fail-safe, lanjutkan tugas (node 13).

---

## 16. PERFORMANCE OPTIMIZATION

**Metrik yang diukur:** `TOKEN`, `LATENCY`, `RESOURCE`.

**Mode adaptif:**
```
FULL MODE        (resource cukup)
  ↓ resource terbatas
OPTIMIZED MODE   (potong verbose, batch tool call)
  ↓ kritis
LOW RESOURCE MODE (ringkas, eskalasi cepat)
```

**Prioritas:** `TASK > SAFETY > RELIABILITY > observability berlebihan`. Jangan bakar token untuk log yang tak perlu.

**Anti-pattern:** memanggil tool berulang untuk data yang sudah ada (pemborosan token/latency).

---

## 17. SELF-IMPROVEMENT

**Loop:**
```
USE → OBSERVE → EVALUATE → FIND WEAKNESS → IMPROVE → TEST → NEW VERSION
```

**Batasan ketat:** **jangan ubah diri sendiri membabi buta.** Setiap upgrade harus lewat:
1. Evaluasi (node 14) yang menemukan kelemahan nyata.
2. Regression test (jalankan compliance matrix node 21-appendix).
3. Version bump sesuai node 18.

**Failure mode:** mutasi struktur tanpa test → node hilang, compliance rusak.

---

## 18. VERSIONING

- **SemVer:** `MAJOR.MINOR.PATCH`.
  - Perubahan **struktur** (tambah/hapus node) = **MAJOR**.
  - Penambahan panduan/perbaikan tanpa ubah struktur = **MINOR**.
  - Perbaikan wording/typo = **PATCH**.
- **CHANGELOG wajib** (lihat node 21 / Appendix A).
- Upgrade skill warisan: restruktur ke 21-node dulu, lalu bump versi.

**Template CHANGELOG:**
```
## [1.1.0] - YYYY-MM-DD
### Added
- <elemen pro baru>
### Changed
- <peningkatan node X>
### Fixed
- <fluff/bug dihilangkan>
```

---



**CHANGELOG**
- 1.0.0 — Light upgrade: frontmatter `description` diperbaiki jadi trigger nyata; Node 2 (PURPOSE) & Node 3 (METADATA) diisi bila stub; `metadata.openclaw.version` diset. Body domain dipertahankan.
- 1.1.1 — Fix frontmatter (description dipisah dari metadata), hapus homoglyph CJK (而非), bump 1.1.1.
- 1.1.2 — Turunkan claim otoritas (wajib/mutlak → recommended/rujukan); kriteria penolakan otomatis jadi rekomendasi review. Kepatuhan SkillSpector (authority overstatement).
## 19. COMPATIBILITY

Skill tahu batasnya: `OS`, `ARCHITECTURE`, `RUNTIME`, `VERSION`, `AVAILABLE TOOL`, `AVAILABLE API`.

**Contoh kritis:**
```
Android ARM64 + Termux   ≠   Ubuntu x86_64
(tanpa systemd)               (systemd tersedia)
```

Setiap skill mendeklarasikan matriks kompatibilitas di metadata/context. Bila input berada di luar matriks → gunakan alternatif (node 12) atau tolak dengan penjelasan (node 6).

---

## 20. KNOWLEDGE SOURCES

**Hierarki kepercayaan (trust hierarchy):**
```
OFFICIAL DOCUMENTATION  (tertinggi)
  ↓
PRIMARY SOURCE          (kode/resmi project)
  ↓
REPUTABLE TECH SOURCE   (dokumen teknis terpercaya)
  ↓
COMMUNITY               (forum, diskusi)
  ↓
UNKNOWN                 (tanpa rujukan)
```

**Tagi setiap sumber:** `VERIFIED / LIKELY / UNCERTAIN / OUTDATED / CONFLICTING`.

**Aturan:** sumber `UNKNOWN`/`CONFLICTING` wajib dikonfirmasi sebelum dijadikan keputusan `CONFIRMED`.

**Anti-pattern:** mengutip community tanpa verifikasi sebagai fakta mutlak.

---

## 21. EXIT CONDITIONS

Skill wajib tahu kapan **berhenti** (paling sering dilupakan — penyebab loop).

| Kondisi | Tindakan saat exit |
|---------|--------------------|
| SUCCESS | Laporkan hasil + bukti verifikasi |
| FAILURE | Laporkan diagnosis + apa yang sudah dicoba |
| BLOCKED | Jelaskan penghalang, serahkan ke user |
| NEED USER | Ajukan pertanyaan klarifikasi spesifik |
| NEED CREDENTIAL | Minta kredensial (jangan log) |
| NEED TOOL | Sebutkan tool yang kurang |
| NEED VERIFICATION | Minta user konfirmasi eksternal |

**Tanpa exit condition, agent akan looping.** Setiap runbook (node 8) harus berujung pada salah satu kondisi di atas.

---

# APPENDIX A — 15 PRINSIP INTI (COMPLIANCE MATRIX)

| # | Prinsip | Node wajib |
|---|---------|-----------|
| 1 | Trigger Intelligence | 4. Trigger Engine |
| 2 | Context Awareness | 5. Context Engine |
| 3 | Decision Policy (IF/THEN) | 6. Decision Policy |
| 4 | Verification Engine | 11. Verification Engine |
| 5 | Recovery Strategy | 12. Error Recovery |
| 6 | Risk Classification | 6 + 13 (LOW/MEDIUM/HIGH/CRITICAL) |
| 7 | Tool Selection Policy | 9. Tool Policy |
| 8 | Knowledge Hierarchy | 20. Knowledge Sources |
| 9 | Self-Evaluation | 14. Evaluation |
| 10 | Observability Hooks | 15. Observability |
| 11 | Memory Policy | 10. Memory Policy |
| 12 | Self-Improvement Loop | 17. Self-Improvement |
| 13 | Compatibility Layer | 19. Compatibility |
| 14 | Resource Awareness | 16. Performance Optimization |
| 15 | Exit Conditions | 21. Exit Conditions |

Risk Classification standar:
```
READ FILE        → LOW
INSTALL PACKAGE  → MEDIUM
MODIFY CONFIG    → MEDIUM
DELETE DATABASE  → CRITICAL
```
Semakin tinggi risiko → semakin ketat verifikasi + approval.

---

# APPENDIX B — TEMPLATE EKSPANSI 30-NODE (CHECKLIST AUDIT)

Gunakan ini untuk audit skill lama. Setara dengan 21-node di atas, hanya lebih rinci:

```
IDENTITY
MISSION
SCOPE
METADATA
TRIGGERS
CONTEXT
PRECONDITIONS
KNOWLEDGE
KNOWLEDGE SOURCES
DECISION POLICY
REASONING POLICY
TOOL POLICY
EXECUTION POLICY
RESOURCE POLICY
VERIFICATION
ERROR HANDLING
RECOVERY
FALLBACK
SECURITY
PERMISSION
RISK CONTROL
MEMORY
OBSERVABILITY
EVALUATION
SELF-IMPROVEMENT
VERSIONING
COMPATIBILITY
SUCCESS CONDITIONS
FAILURE CONDITIONS
EXIT CONDITIONS
CHANGELOG
```

---

# APPENDIX C — ENFORCEMENT RULE (WAJIB UNTUK AGENT)

Setiap kali agent akan:
- **Membuat skill baru** → struktur wajib 21-node + lulus compliance matrix (Appendix A).
- **Upgrade skill lama** → restruktur ke 21-node, lalu bump versi sesuai node 18.
- **Review skill** → jalankan checklist Appendix B; tolak bila node wajib hilang atau description tidak trigger-centric.
- **Self-improvement** → ikuti batasan node 17 (evaluasi + regression test, bukan mutasi buta).

**Kriteria review yang disarankan (bukan penolakan otomatis):**
1. Node 21 sebisa mungkin lengkap; jika kurang, catat sebagai rekomendasi perbaikan.
2. `description` disarankan menyebutkan pola aktivasi user.
3. Disarankan ada decision policy (node 6) dan verification engine (node 11).
4. Jangan sertakan PII (email, URL repo pribadi, token) — lihat node 13.
