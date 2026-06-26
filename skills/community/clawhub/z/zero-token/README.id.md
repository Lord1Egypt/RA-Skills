## Agent Kamu Pernah Diam?

Saldo API habis. DeepSeek kena rate limit. OpenAI down. Agent-mu sudah 80% selesai — lalu diam.

Pengguna tidak paham infrastruktur. Mereka cuma tahu "rusak lagi". Tiga kali dan mereka pergi.

---

## Yang Dilakukan Zero Token

Bukan "rencana cadangan". Bukan "mode degradasi". Ini **ambil alih tak terlihat**.

Begitu model utama mati, 13 LLM gratis sudah berjalan. Kepribadian sama. Keputusan sama. Suara sama. Pengguna tidak sadar ada peralihan.

**Rp0. Nol downtime. Nol deteksi.**

---

## Dua Baris. Satu Menit.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

Gateway [Free-Way](https://github.com/GoDiao/Free-Way) menggabungkan 13+ penyedia LLM gratis di balik satu endpoint `/v1`. OpenClaw menggunakannya sebagai fallback. Model utama mati? → Auto switch. Agent tetap jalan.

---

## Dua Mode

| Mode | Kondisi | Hasil |
|------|---------|-------|
| 🆓 Mode Gratis | Tanpa API key berbayar | Agent jalan di model gratis, kepribadian SOUL utuh |
| 🛡️ Mode Ambil Alih | Model utama mati / token habis | Auto switch ke penyedia gratis, kerja lanjut |

---

## Transparansi Penuh

Zero Token tidak pernah menyembunyikan peralihan. Saat fallback aktif, agent-mu berjalan di penyedia gratis — bukan model utama. Setiap penyedia punya kebijakan privasi dan retensi data sendiri. **Tinjau ketentuan setiap penyedia sebelum mengirim data sensitif.** Skrip setup menampilkan dengan jelas penyedia mana yang dikonfigurasi. Kamu yang mengontrol kunci.

> 💡 Ini failover transparan, dikendalikan olehmu. Kamu pegang kunci. Kamu pilih penyedia.

---

## Gratis ≠ Sampah

Output mentah model gratis biasa saja. Tapi dengan DNA perilaku `::GENE{}` di atasnya — kepribadian sama, keputusan sama, nada sama. Tidak ada yang bisa bedakan DeepSeek V4 Pro atau Llama 3.3 70B.

---

## Kenapa Gratis

Free-Way + Zero Token open source. Setiap penyedia punya tingkat gratis:

| Penyedia | Batas Gratis | Model Terbaik |
|----------|-------------|--------------|
| Groq | 1000 req/hari | Llama 3.3 70B |
| Gemini Flash | 1500 req/hari | Gemini 2.5 Flash |
| Cerebras | 1700 req/hari | Llama 3.3 70B |
| Cloudflare | 10k neurons/hari | Llama 3.1 8B |
| OpenRouter | 200 req/hari | Beberapa model gratis |
| Mistral | 1 req/detik | Mistral Small |
| Cohere | 20 req/menit | Command R+ |
| NVIDIA NIM | Tingkat gratis | Llama 3.3 70B |

Setiap key perlu 30 detik. Script setup memandu kamu.

---

## Perbandingan

| | Setup Biasa | Zero Token |
|---|---|---|
| Biaya Model | $0.14–$15.00/M tokens | **$0.00** |
| Saat Gangguan | Berhenti total | Failover tak terlihat |
| Model Cadangan | 0 | 13+ |
| Kepribadian Agent | Hilang saat fallback | Selalu konsisten |
| Waktu Setup | Setengah hari (load balancing) | 1 menit |

---

## Kapan Upgrade

Zero Token menjaga kamu tetap online. Untuk kualitas output terbaik — DeepSeek V4 Pro + genom lengkap, harga 3% dari Opus:

```bash
openclaw skills install poor-mans-opus
```
