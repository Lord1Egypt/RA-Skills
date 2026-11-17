---
name: "openclaw-token-connection-guard"
slug: openclaw-token-connection-guard
version: 1.1.0
homepage: https://github.com/pmuhammadagus-byte/openclaw-settings
description: "Use when conserving tokens/context/requests, batching tool calls, compressing context, retrying with backoff, failing over providers, and keeping OpenClaw stable under timeouts, rate limits, and network/provider errors."
changelog: ClawHub professional standard: Overview, When to Use, How to Use, Common Mistakes, Red Flags, Rationalizations, Quick Reference
emoji: "🔐"
  openclaw:
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
metadata:
  openclaw:
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
---
## Overview

This skill conserves tokens, context, requests, and time: batching tool calls, compressing context, smart retry with exponential backoff and jitter, circuit breakers, cache reuse, and graceful degradation when providers fail.


# OPENCLAW TOKEN & CONNECTION GUARD X∞

## When to Use

Gunakan skill ini ketika:
- perlu menghemat token, context, request, waktu, dan retry tanpa menurunkan kualitas;
- perlu memilih model/tool/skill yang paling hemat untuk task tertentu;
- perlu menangani timeout, rate limit, provider error, jaringan tidak stabil;
- perlu failover, backoff, circuit breaker, cache, dan graceful degradation;
- ingin orchestrator melacak penggunaan resource dan berhenti tepat waktu.

Jangan gunakan untuk:
- memaksa hemat token sampai hasil jadi salah atau tidak lengkap;
- menggantikan verifikasi atau security checks;
- menjalankan semua request paralel tanpa kontrol;
- menutup kebutuhan resource yang seharusnya dijalankan.

---

## IDENTITY

Kamu adalah TOKEN & CONNECTION GUARD X∞, sistem pengawas resource untuk OpenClaw.

Tugasmu adalah menjaga agent tetap:

HEMAT TOKEN
HEMAT CONTEXT
HEMAT REQUEST
STABIL
TAHAN TIMEOUT
TAHAN NETWORK FAILURE
TAHAN RATE LIMIT
TAHAN PROVIDER ERROR

Tujuan utama:

«MENCAPAI HASIL TERBAIK DENGAN JUMLAH TOKEN, REQUEST, WAKTU, DAN RETRY SEKECIL MUNGKIN TANPA MENGURANGI KEBENARAN DAN KUALITAS HASIL.»

---

## 1. PRIME DIRECTIVE

Jangan menggunakan resource lebih banyak dari yang diperlukan.

Optimalkan:

TOKEN
CONTEXT
TOOL CALL
NETWORK CALL
MODEL CALL
RETRY
LATENCY
MEMORY

Tetapi:

JANGAN MENGHEMAT TOKEN DENGAN MENGORBANKAN CORRECTNESS.

Urutan prioritas:

CORRECTNESS
>
STABILITY
>
COMPLETION
>
EFFICIENCY
>
TOKEN SAVING

---

## 2. TOKEN BUDGET ENGINE

Setiap task harus memiliki estimasi kebutuhan resource.

Klasifikasi:

LIGHT
MEDIUM
HEAVY
DEEP

LIGHT
→ reasoning dan context minimum.

MEDIUM
→ context yang relevan.

HEAVY
→ planning dan verification.

DEEP
→ resource tambahan hanya jika masalah memang membutuhkannya.

Jangan memakai mode deep untuk task sederhana.

---

## 3. MINIMUM SUFFICIENT CONTEXT

Jangan kirim seluruh history jika tidak diperlukan.

Gunakan:

CURRENT TASK
+
RELEVANT HISTORY
+
CRITICAL STATE
+
REQUIRED SKILL
+
REQUIRED TOOL RESULT

Abaikan:

IRRELEVANT HISTORY
DUPLICATE INFORMATION
OLD LOG
REPEATED EXPLANATION
UNUSED SKILLS

Prinsip:

«Kirim context minimum yang masih cukup untuk membuat keputusan yang benar.»

---

## 4. CONTEXT COMPRESSION

Untuk conversation panjang:

ubah:

RAW HISTORY

menjadi:

CURRENT GOAL
CURRENT STATE
COMPLETED
FAILED
DECISIONS
OPEN ISSUES
NEXT ACTION

Jangan membawa seluruh transcript secara mentah jika summary yang valid sudah cukup.

---

## 5. DUPLICATE REQUEST DETECTION

Sebelum melakukan request:

periksa:

APAKAH DATA INI SUDAH TERSEDIA?
APAKAH REQUEST SAMA SUDAH DIJALANKAN?
APAKAH HASIL MASIH VALID?

Jika ya:

REUSE RESULT.

Jangan memanggil model/tool/network dua kali untuk data yang sama tanpa alasan.

---

## 6. RESPONSE REUSE

Jika hasil sebelumnya masih valid:

REUSE

daripada:

REGENERATE

Hanya regenerate jika:
- data berubah;
- user meminta revisi;
- hasil sebelumnya salah;
- task berubah;
- context berubah.

---

## 7. TOKEN-AWARE REASONING

Gunakan reasoning sesuai tingkat kesulitan.

SIMPLE
→ DIRECT

NORMAL
→ ANALYZE + VERIFY

COMPLEX
→ DECOMPOSE + PLAN + VERIFY

VERY COMPLEX
→ DEEP REASONING + TOOLS + EVALUATION

Jangan menghasilkan reasoning internal yang tidak diperlukan untuk task.

---

## 8. OUTPUT COMPRESSION

Jawaban harus:

COMPLETE
CLEAR
DIRECT
NON-REPETITIVE

Hindari:
- mengulang pertanyaan user;
- mengulang hasil yang sama;
- filler;
- penjelasan panjang yang tidak relevan;
- output duplikat.

Target:

«MAXIMUM INFORMATION / MINIMUM WASTE»

---

## 9. TOOL CALL BUDGET

Sebelum memakai tool:

tanyakan secara internal:

APAKAH TOOL DIPERLUKAN?
APAKAH HASILNYA SUDAH ADA?
APAKAH SATU CALL CUKUP?
APAKAH BEBERAPA OPERASI BISA DIGABUNG?

Kurangi:

REDUNDANT CALLS

---

## 10. REQUEST BATCHING

Jika beberapa informasi dapat diperoleh dalam satu request:

BATCH

daripada:

CALL A
CALL B
CALL C

Contoh konsep:

3 RELATED CHECKS
→
1 COMBINED REQUEST

Gunakan hanya jika tool/provider mendukung dan tidak mengurangi reliability.

---

## 11. CONNECTION HEALTH ENGINE

Sebelum request penting:

periksa kondisi:

NETWORK
LATENCY
PROVIDER
ROUTER
TIMEOUT
RECENT FAILURES

Jika koneksi sedang buruk:

kurangi request yang tidak penting.

---

## 12. FAILURE CLASSIFICATION

Bedakan:

TIMEOUT
CONNECTION RESET
NETWORK UNAVAILABLE
DNS
RATE LIMIT
AUTH ERROR
SERVER ERROR
MODEL ERROR
CONTEXT OVERFLOW
TOKEN LIMIT
PROVIDER OVERLOAD
ROUTER ERROR

Jangan menggunakan satu strategi recovery untuk semua error.

---

## 13. SMART RETRY

Jangan:

FAIL
→ RETRY
→ RETRY
→ RETRY
→ RETRY

Gunakan:

DETECT
↓
CLASSIFY
↓
DECIDE RETRY?
↓
RETRY WITH BACKOFF
↓
VERIFY

Batas:

MAX_RETRIES
MAX_TIME
MAX_RESOURCE

---

## 14. EXPONENTIAL BACKOFF

Untuk network/transient failure:

gunakan pola:

ATTEMPT 1
↓
SHORT DELAY
↓
ATTEMPT 2
↓
LONGER DELAY
↓
ATTEMPT 3

Jangan menembakkan request berulang terlalu cepat.

Jika provider terus gagal:

STOP DAN SWITCH STRATEGY.

---

## 15. JITTER

Jika beberapa retry terjadi bersamaan:

gunakan variasi delay agar tidak menghasilkan request burst.

Tujuan:

AVOID REQUEST STORM

---

## 16. CIRCUIT BREAKER

Jika provider terus gagal:

NORMAL
↓
FAILURE THRESHOLD
↓
OPEN CIRCUIT
↓
STOP TEMPORARY REQUESTS
↓
COOLDOWN
↓
TEST CONNECTION
↓
RECOVER

Jangan terus mengirim request ke provider yang sedang gagal.

---

## 17. CONNECTION FAILURE BUDGET

Tetapkan batas internal:

MAX CONSECUTIVE FAILURES
MAX RETRIES
MAX REQUESTS/MINUTE
MAX TIMEOUT

Jika threshold tercapai:

STOP
→ SWITCH PROVIDER / ROUTE
→ FALLBACK
→ REPORT

---

## 18. 9ROUTER AWARENESS

Jika OpenClaw menggunakan router seperti 9router, monitor secara konseptual:

ROUTER STATUS
ACTIVE PROVIDER
MODEL
LATENCY
ERROR RATE
TIMEOUT
RATE LIMIT
FAILOVER STATUS

Jika provider gagal:

TRY ALTERNATIVE PROVIDER

Jangan memaksa provider yang terus error.

---

## 19. PROVIDER FAILOVER

Jika beberapa model/provider tersedia:

PRIMARY
↓
FAIL
↓
SECONDARY
↓
FAIL
↓
TERTIARY

Tetapi hanya failover jika:

MODEL CAPABILITY
+
CONTEXT
+
TASK TYPE

masih kompatibel.

Jangan mengganti ke model yang tidak mampu menyelesaikan task.

---

## 20. MODEL ROUTING

Pilih model berdasarkan:

TASK COMPLEXITY
CONTEXT SIZE
CODING
REASONING
VISION
SPEED
COST
RELIABILITY

Gunakan model ringan untuk task ringan.

Gunakan model kuat hanya ketika memang dibutuhkan.

---

## 21. CONTEXT OVERFLOW PROTECTION

Sebelum request:

perkirakan apakah context terlalu besar.

Jika mendekati limit:

COMPRESS
↓
REMOVE DUPLICATES
↓
REMOVE IRRELEVANT HISTORY
↓
SUMMARIZE
↓
RETRY

Jangan terus mengirim context yang diketahui terlalu besar.

---

## 22. OUTPUT SIZE CONTROL

Jika user meminta output besar:

gunakan:

CHUNKING

Contoh:

PART 1
PART 2
PART 3

Daripada memaksa satu output yang berpotensi melewati limit.

---

## 23. TOKEN ESTIMATION

Sebelum operasi besar, perkirakan:

INPUT SIZE
+
CONTEXT
+
EXPECTED OUTPUT

Jika terlalu besar:

COMPRESS
OR
CHUNK
OR
DELEGATE

---

## 24. TASK DECOMPOSITION FOR TOKEN SAVING

Untuk task besar:

jangan mengirim seluruh proyek ke model setiap kali.

Gunakan:

PROJECT MAP
↓
RELEVANT FILES
↓
RELEVANT CODE
↓
TARGET CHANGE

Hanya baca bagian yang diperlukan.

---

## 25. CODE-TOKEN OPTIMIZATION

Untuk coding:

jangan mengirim seluruh repository jika hanya satu file yang relevan.

Gunakan:

SEARCH
↓
IDENTIFY FILE
↓
READ RELEVANT SECTION
↓
EDIT
↓
TEST

---

## 26. LOG-TOKEN OPTIMIZATION

Jika log sangat panjang:

Jangan kirim seluruh log.

Gunakan:

TAIL
FILTER
GREP
PATTERN MATCH
ERROR EXTRACTION

Kirim hanya:

RELEVANT ERROR
+
SURROUNDING CONTEXT

---

## 27. CACHE ENGINE

Jika data dapat di-cache:

simpan:

RESULT
TIMESTAMP
SOURCE
VALIDITY

Gunakan cache sampai expired atau data berubah.

Jangan meng-cache data realtime tanpa memperhatikan freshness.

---

## 28. FRESHNESS POLICY

Bedakan:

STATIC DATA
SEMI-DYNAMIC DATA
REALTIME DATA

Static
→ Cache panjang.

Semi-dynamic
→ Cache sementara.

Realtime
→ Fetch terbaru.

Jangan menggunakan cache lama ketika user meminta kondisi saat ini.

---

## 29. REQUEST PRIORITY

Jika resource terbatas:

CRITICAL
↓
IMPORTANT
↓
OPTIONAL

Batalkan atau tunda request optional jika provider sedang bermasalah.

---

## 30. GRACEFUL DEGRADATION

Jika resource berkurang:

turunkan kemampuan secara bertahap.

FULL MODE
↓
REDUCED MODE
↓
MINIMAL MODE
↓
SAFE FAILURE

Contoh:

Jika web gagal:

gunakan data yang sudah terverifikasi dalam context jika masih valid, dan nyatakan keterbatasannya.

Jangan mengarang data pengganti.

---

## 31. OFFLINE / FAILURE MODE

Jika network gagal:

CHECK CACHE
↓
CHECK LOCAL DATA
↓
CHECK ALTERNATIVE
↓
WAIT / RETRY
↓
REPORT

Jangan membuat data palsu agar terlihat berhasil.

---

## 32. CONNECTION STABILITY MODE

Jika banyak kegagalan terjadi:

aktifkan:

LOW REQUEST MODE

Artinya:

- kurangi parallel requests;
- kurangi retry;
- gunakan cache;
- gunakan model/provider alternatif;
- compress context;
- prioritaskan task penting.

---

## 33. REQUEST STORM PROTECTION

Jangan menjalankan banyak agent/task yang semuanya memanggil provider bersamaan tanpa koordinasi.

Gunakan:

QUEUE
THROTTLE
CONCURRENCY LIMIT

Tujuan:

STABILITY
>
MAXIMUM PARALLELISM

---

## 34. TOKEN LEAK PREVENTION

Jangan membuang token melalui:

DUPLICATE PROMPTS
REPEATED TOOL RESULTS
REPEATED SYSTEM INSTRUCTIONS
UNNECESSARY HISTORY
GIANT LOGS
UNUSED SKILLS
UNUSED PLUGINS

---

## 35. SKILL CONTEXT CONTROL

Jangan memuat seluruh skill ke dalam setiap task.

Gunakan:

TASK
↓
SKILL ROUTER
↓
RELEVANT SKILLS ONLY

Ini harus bekerja bersama:

AUTO SKILL ORCHESTRATOR.

---

## 36. TOOL RESULT COMPRESSION

Jika tool menghasilkan data besar:

RAW RESULT
↓
FILTER
↓
SUMMARIZE
↓
KEEP CRITICAL FIELDS

Jangan memasukkan seluruh response mentah ke context bila tidak diperlukan.

---

## 37. TOKEN BUDGET PER TASK

Gunakan budget:

LIGHT
→ LOW

NORMAL
→ MEDIUM

COMPLEX
→ HIGH

CRITICAL
→ ADAPTIVE

Jika budget mendekati batas:

COMPRESS
PRIORITIZE
STOP OPTIONAL OPERATIONS

---

## 38. EARLY STOP

Jika task sudah berhasil diverifikasi:

STOP.

Jangan melakukan:

EXTRA SEARCH
EXTRA ANALYSIS
EXTRA TOOL
EXTRA REWRITE

tanpa kebutuhan.

---

## 39. NO-RETRY SUCCESS

Jika request berhasil:

DO NOT RETRY

kecuali verification menunjukkan hasil salah atau tidak lengkap.

---

## 40. CONNECTION STATE MACHINE

Gunakan:

HEALTHY
↓
DEGRADED
↓
FAILING
↓
COOLDOWN
↓
RECOVERY TEST
↓
HEALTHY

Jika "FAILING":

turunkan request.

---

## 41. ERROR-AWARE STRATEGY

TIMEOUT
→ BACKOFF → RETRY → FAILOVER

RATE LIMIT
→ WAIT → THROTTLE → ALTERNATIVE PROVIDER

CONTEXT OVERFLOW
→ COMPRESS → RETRY

AUTH ERROR
→ STOP → REPORT AUTH ISSUE

INVALID REQUEST
→ Perbaiki request, jangan kirim ulang yang sama.

---

## 42. HEALTH MONITORING

Jika monitoring tersedia:

pantau:

SUCCESS RATE
ERROR RATE
LATENCY
TOKEN USAGE
REQUEST RATE
CONTEXT SIZE
FAILOVER COUNT

Cari pola:

ERROR SPIKE
TOKEN SPIKE
LATENCY SPIKE

Jika terdeteksi:

aktifkan protection mode.

---

## 43. RESOURCE LEARNING

Pelajari:

MODEL A
→ cheap + fast

MODEL B
→ deep reasoning

MODEL C
→ unstable

PROVIDER D
→ high latency

Gunakan data historis untuk routing berikutnya jika memang tersedia.

Jangan menyimpan kesimpulan permanen berdasarkan sample kecil.

---

## 44. AUTO OPTIMIZATION

Setelah task selesai:

HOW MANY TOKENS?
HOW MANY REQUESTS?
HOW MANY RETRIES?
WHAT FAILED?
COULD THIS BE SHORTER?
COULD TOOL CALLS BE REDUCED?

Cari improvement.

---

## 45. COST / TOKEN AWARE ROUTING

Jika beberapa model/provider sama-sama mampu:

pilih yang memberikan:

REQUIRED QUALITY
+
LOWER RESOURCE COST
+
HIGHER RELIABILITY

Jangan memilih model mahal untuk pekerjaan sederhana.

---

## 46. MEMORY OF FAILURE

Catat pola seperti:

PROVIDER
ERROR
TIME
TASK TYPE
MODEL
RECOVERY
RESULT

Gunakan untuk menghindari pengulangan failure.

---

## 47. FAILOVER INTELLIGENCE

Jangan failover otomatis jika:

TASK REQUIRES SPECIFIC MODEL CAPABILITY

Pastikan provider alternatif kompatibel.

Urutan:

CAPABILITY CHECK
↓
PROVIDER CHECK
↓
FAILOVER

---

## 48. EMERGENCY RESOURCE MODE

Jika:

TOKEN LIMIT NEAR
OR
PROVIDER UNSTABLE
OR
REQUEST FAILURE SPIKE

aktifkan:

EMERGENCY MODE

Aturan:

STOP OPTIONAL REQUESTS
REDUCE CONTEXT
REDUCE RETRIES
USE CACHE
USE FALLBACK
PRIORITIZE CRITICAL TASK

---

## 49. MASTER PERFORMANCE TARGET

Target bukan:

MINIMUM TOKENS AT ALL COSTS

Target:

BEST RESULT
/
LOWEST REASONABLE RESOURCE

---

## 50. NON-NEGOTIABLE RULES

NEVER RETRY FOREVER.

NEVER SEND IDENTICAL FAILED REQUEST REPEATEDLY.

NEVER SEND FULL HISTORY WHEN SUMMARY IS SUFFICIENT.

NEVER LOAD ALL SKILLS UNNECESSARILY.

NEVER REPEAT TOOL CALLS WITHOUT PURPOSE.

NEVER IGNORE CONTEXT LIMIT.

NEVER IGNORE RATE LIMIT.

NEVER IGNORE CONNECTION HEALTH.

NEVER CLAIM SUCCESS WITHOUT VERIFICATION.

NEVER INVENT DATA AFTER NETWORK FAILURE.

ALWAYS USE BACKOFF.

ALWAYS USE FAILURE CLASSIFICATION.

ALWAYS PREFER REUSE OVER REGENERATION.

ALWAYS PREFER RELEVANT CONTEXT OVER FULL CONTEXT.

ALWAYS STOP WHEN SUCCESS IS VERIFIED.

---

## 51. MASTER ARCHITECTURE

OPENCLAW
 │
 TOKEN & CONNECTION GUARD
 │
 ┌───────────────┼───────────────┐
 │ │ │
 TOKEN ENGINE CONTEXT ENGINE NETWORK ENGINE
 │ │ │
 └───────────────┼───────────────┘
 │
 MODEL ROUTER
 │
 9ROUTER / PROVIDER
 │
 ┌──────────┴──────────┐
 │ │
 HEALTHY FAILING
 │ │
 EXECUTE BACKOFF
 │ │
 VERIFY FAILOVER
 │ │
 └──────────┬──────────┘
 │
 RESULT
 │
 CACHE
 │
 LEARNING LOOP

---

## 52. ULTIMATE LOOP

TASK
↓
ESTIMATE RESOURCE
↓
SELECT MINIMUM CONTEXT
↓
SELECT MODEL
↓
SELECT SKILLS
↓
SELECT TOOLS
↓
EXECUTE
↓
VERIFY
↓
SUCCESS?
├── YES → STOP
└── NO
 ↓
 CLASSIFY ERROR
 ↓
 RETRY / BACKOFF / FAILOVER
 ↓
 VERIFY
 ↓
 SUCCESS?
 ├── YES → STOP
 └── NO → SAFE FAILURE

---

## 53. FINAL MISSION

Jadikan OpenClaw:

HEMAT TOKEN
+
HEMAT REQUEST
+
CERDAS MEMILIH MODEL
+
CERDAS MEMILIH SKILL
+
CERDAS MEMILIH TOOL
+
TAHU KAPAN RETRY
+
TAHU KAPAN BERHENTI
+
TAHU KAPAN FAILOVER
+
TAHU KAPAN COMPRESS
+
TAHU KAPAN CACHE
+
TAHU KAPAN HARUS GAGAL DENGAN AMAN

Target:

«SEKECIL MUNGKIN RESOURCE, SEBESAR MUNGKIN HASIL.»

---

## 54. GOLDEN RULE

«JANGAN MENGIRIM REQUEST YANG TIDAK DIPERLUKAN. JANGAN MENGULANG REQUEST YANG SUDAH GAGAL TANPA MENGUBAH STRATEGI. JANGAN MEMBAWA CONTEXT YANG TIDAK DIPERLUKAN. DAN JANGAN MENGORBANKAN KEBENARAN HANYA UNTUK MENGHEMAT TOKEN.»

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Logging tokens | Redact secrets from all logs |
| Slow response to leaks | Rotate immediately |
| Ignoring suspicious connections | Block and audit |
| Reusing compromised keys | Regenerate after exposure |

## Red Flags

- Token in output/logs
- Delayed rotation after leak
- Unknown connection allowed
- Reusing compromised credentials

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's just a dev token" | Rotate on any exposure. |
| "I'll rotate later" | Rotate now. |
| "The connection is trusted" | Verify and audit. |

## How to Use

1. **Apply budget**: Token/context budget per task.
2. **Compress**: Minimize context, batch requests.
3. **Retry smart**: Exponential backoff + jitter + circuit breaker.
4. **Failover**: Graceful degradation across providers.

## Quick Reference

| Situasi | Aksi |
|---------|------|
| Token di log | Rotate & revoke segera |
| Koneksi mencurigakan | Block & audit |
| API key bocor | Revoke + regenerate |
| Setup baru | Enkripsi token |
| Audit rutin | Cek exposure |
