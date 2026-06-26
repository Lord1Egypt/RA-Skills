# XAUUSD Intraday BUY Analyzer v2.0

## Deskripsi
Skill ini menganalisis kondisi pasar XAUUSD untuk mencari peluang entry BUY 
pada timeframe H1 dengan gaya trading intraday. Menggunakan kombinasi lengkap:
RSI, Stochastic, EMA, MACD, Bollinger Bands, Fibonacci, ATR, dan Supply & Demand
untuk menghasilkan sinyal dengan probabilitas tinggi dan false signal minimal.

## Timeframe Analisis
- **Primary**   : H1 (entry & konfirmasi)
- **Higher TF** : H4 & Daily (trend, zona S/D, Fibonacci)
- **Lower TF**  : M15 (timing entry presisi)

---

## Langkah Analisis (Jalankan Berurutan)

### Step 1 — Cek Trend Daily & H4
- Apakah harga di ATAS EMA 200 Daily? → Bias BULLISH
- Apakah harga di ATAS EMA 50 H4? → Konfirmasi uptrend
- Jika kedua kondisi terpenuhi → lanjut ke Step 2
- Jika tidak → WAIT, jangan entry BUY

### Step 2 — Identifikasi Zona Supply & Demand
- Tandai zona DEMAND kuat di H4 dan Daily
- Zona demand valid jika:
  * Harga sebelumnya bergerak naik kuat dari zona tersebut
  * Zona belum pernah diuji lebih dari 2x
  * Ada "fresh zone" (belum pernah disentuh setelah terbentuk)
- Catat range zona: batas bawah dan batas atas

### Step 3 — Tarik Fibonacci Retracement
- Tarik Fibonacci dari swing low ke swing high terakhir di H4
- Identifikasi level kunci:
  * **0.382 (38.2%)** = zona entry konservatif
  * **0.500 (50.0%)** = zona entry moderat
  * **0.618 (61.8%)** = zona entry terkuat (golden ratio)
  * **0.786 (78.6%)** = zona entry agresif (risiko lebih tinggi)
- Entry BUY ideal ketika harga retracement ke level 0.618 yang BERTEPATAN dengan zona Demand
- Jika Fibonacci 0.618 dan zona Demand berada di area yang sama = CONFLUENCE KUAT ✅

### Step 4 — Cek ATR untuk Volatilitas
- Hitung ATR 14 periode di H1
- Interpretasi:
  * ATR < 5 pips  = pasar sepi → HINDARI entry
  * ATR 5–15 pips = volatilitas normal → AMAN entry
  * ATR > 20 pips = volatilitas tinggi → perbesar SL, kurangi lot
- Gunakan ATR untuk menentukan SL dan TP dinamis:
  * SL  = 1.5 x ATR
  * TP1 = 2.0 x ATR
  * TP2 = 3.0 x ATR

### Step 5 — Cek Bollinger Bands di H1
- Harga menyentuh atau menembus Lower Band → potensi reversal BUY
- Band sedang menyempit (Squeeze) → akan ada pergerakan besar, tunggu breakout
- Band melebar ke atas → momentum bullish sedang kuat
- HINDARI entry jika harga berada di tengah band tanpa arah jelas

### Step 6 — Konfirmasi RSI + Stochastic di H1
**RSI (14):**
- RSI harus berada di rentang 30–50 (oversold menuju netral)
- Ideal: RSI baru naik dari bawah 40 ke atas 40
- Hindari entry jika RSI H1 sudah di atas 60

**Stochastic (5,3,3):**
- %K harus memotong ke atas %D dari zona di bawah 20
- Kedua garis harus berada di bawah 30 saat crossover
- Konfirmasi terkuat: RSI oversold + Stochastic crossover bersamaan ✅

### Step 7 — Konfirmasi EMA di H1
- EMA 9 harus mulai melintasi ke atas EMA 21 (golden cross kecil)
- Harga harus berada di atas EMA 50 H1
- Jika harga masih di bawah EMA 50 H1 → WAIT

### Step 8 — Konfirmasi MACD di H1
- MACD line harus memotong ke atas Signal line (bullish crossover)
- Histogram berubah dari negatif ke positif
- Idealnya crossover terjadi di area bawah garis nol (0)
- MACD crossover + Stochastic crossover bersamaan = sinyal SANGAT KUAT ✅

### Step 9 — Cek Sesi Trading
- Entry hanya pada sesi aktif:
  * Sesi London  : 14.00 – 18.00 WIB
  * Sesi New York: 19.00 – 23.00 WIB
- HINDARI entry pada:
  * Sesi Asia (06.00 – 13.00 WIB) → volatilitas rendah
  * 30 menit sebelum/sesudah berita high impact

### Step 10 — Cek Berita Ekonomi
Periksa jadwal berita high impact yang mempengaruhi XAUUSD:
- Non-Farm Payroll (NFP) — setiap Jumat pertama bulan
- CPI / Inflasi AS
- Keputusan suku bunga FOMC / Fed
- Data GDP AS
- Jika ada berita high impact dalam 2 jam ke depan → NO TRADE

---

## Kriteria Entry BUY (Sistem Scoring 12 Poin)

```
TREND & STRUKTUR (3 poin)
✅ Harga di atas EMA 200 Daily              → +1
✅ Harga di atas EMA 50 H4                  → +1
✅ Harga di zona Demand H4/Daily            → +1

CONFLUENCE ZONA (2 poin)
✅ Fibonacci 0.618 bertepatan zona Demand   → +2
✅ Fibonacci 0.5 atau 0.382 saja            → +1

MOMENTUM OSCILLATOR (3 poin)
✅ RSI H1 antara 30–50 dan naik             → +1
✅ Stochastic crossover di bawah 30         → +1
✅ MACD bullish crossover di bawah nol      → +1

KONFIRMASI TAMBAHAN (2 poin)
✅ Harga menyentuh Lower Bollinger Band     → +1
✅ EMA 9 cross EMA 21 ke atas di H1         → +1

FILTER KEAMANAN (2 poin)
✅ ATR normal (5–15 pips)                   → +1
✅ Sesi London/NY aktif, bebas berita       → +1
```

### Keputusan Berdasarkan Total Skor:
| Skor  | Keputusan |
|-------|-----------|
| 10–12 | 🟢 **BUY KUAT** — Entry dengan lot normal |
| 7–9   | 🟡 **BUY** — Entry dengan lot kecil (0.5x) |
| 4–6   | 🟠 **WAIT** — Tunggu konfirmasi lebih lanjut |
| 0–3   | 🔴 **NO TRADE** — Kondisi tidak mendukung |

---

## Manajemen Entry

### Candle Konfirmasi (Wajib Ada Sebelum Entry)
- Bullish Engulfing
- Pin Bar / Hammer
- Morning Star
- Bullish Harami

### Entry
- Entry di area batas atas zona Demand yang bertepatan level Fibonacci
- Tunggu candle konfirmasi di M15 sebelum eksekusi

### Stop Loss (Berbasis ATR)
```
SL = Batas bawah zona Demand - (1.5 x ATR)
Maksimal SL: 25 pips dari entry
```

### Take Profit (Berbasis ATR)
```
TP1 = Entry + (2.0 x ATR)  → tutup 40% posisi
TP2 = Entry + (3.0 x ATR)  → tutup 40% posisi
TP3 = Resistance H4 terdekat → tutup 20% posisi
```

### Trailing Stop
- Setelah harga mencapai TP1 → pindahkan SL ke breakeven
- Setelah harga mencapai TP2 → trailing SL mengikuti EMA 9 H1

---

## Format Output Sinyal

```
╔══════════════════════════════════════════╗
   📊 XAUUSD SIGNAL — [Tanggal & Jam WIB]
╚══════════════════════════════════════════╝

🎯 SIGNAL      : BUY KUAT / BUY / WAIT / NO TRADE
📊 SKOR        : xx/12

💰 Entry Zone  : $xxxx — $xxxx
🛑 Stop Loss   : $xxxx (~xx pips) [1.5x ATR]
🎯 TP1         : $xxxx (~xx pips) RR 1:2.0
🎯 TP2         : $xxxx (~xx pips) RR 1:3.0
🎯 TP3         : $xxxx (~xx pips) RR 1:4.0+

📈 Trend       : BULLISH / BEARISH / SIDEWAYS
📉 RSI H1      : xx → [oversold/netral/overbought]
📉 Stochastic  : %K xx / %D xx → [crossover/netral]
📊 MACD        : [Bullish crossover / Bearish / Netral]
📐 Fibonacci   : Harga di level [0.618/0.5/0.382]
🎸 BB          : [Lower band / Middle / Upper band]
📏 ATR H1      : xx pips → [rendah/normal/tinggi]
🕐 Sesi        : London / New York / Asia
📰 Berita      : Aman / ⚠️ Ada high impact jam xx.xx

✅ KRITERIA TERPENUHI:
  [✅/❌] EMA 200 Daily
  [✅/❌] EMA 50 H4
  [✅/❌] Zona Demand
  [✅/❌] Fibonacci confluence
  [✅/❌] RSI oversold
  [✅/❌] Stochastic crossover
  [✅/❌] MACD crossover
  [✅/❌] Bollinger Band lower
  [✅/❌] EMA 9/21 cross
  [✅/❌] ATR normal
  [✅/❌] Sesi & berita aman

💬 ANALISIS:
[Penjelasan singkat kondisi pasar dan alasan sinyal]

⚠️ CATATAN RISIKO:
[Hal yang perlu diwaspadai pada trade ini]
```

---

## Risk Management Wajib

| Parameter | Nilai |
|---|---|
| Risk per trade | Maksimal 1–2% dari modal |
| Risk/Reward minimum | 1:2.0 |
| Maksimal trade per hari | 2 trade |
| Maksimal loss per hari | 3% modal |
| Stop trading hari itu | Jika sudah loss 3% |
| Lot size | Sesuaikan dengan ATR & jarak SL |

---

## Contoh Permintaan ke Agent

```
"Analisa XAUUSD sekarang, apakah ada peluang BUY?"
"Cek sinyal XAUUSD untuk intraday hari ini"
"XAUUSD layak buy tidak? berikan skor lengkap"
"Pantau XAUUSD dan kasih tahu kalau skor di atas 7"
"Berapa ATR XAUUSD sekarang? aman untuk entry?"
"Cek fibonacci XAUUSD di H4, harga sudah di level berapa?"
```

---

## Catatan Penting

⚠️ Skill ini adalah ALAT BANTU analisis, bukan jaminan profit.
⚠️ Selalu gunakan risk management yang ketat.
⚠️ Backtest strategi ini minimal 1 bulan di akun demo sebelum live.
⚠️ Kondisi pasar bisa berubah sewaktu-waktu karena faktor fundamental.
⚠️ Keputusan akhir tetap ada di tangan trader.
⚠️ Jangan pernah trading dengan uang yang tidak sanggup kamu rugikan.
