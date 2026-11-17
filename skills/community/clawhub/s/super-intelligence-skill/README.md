# 🧠 Super Intelligence Skill for OpenClaw

Skill ini dirancang untuk **mentransformasi AI Agent apa pun** — meskipun menggunakan model dasar yang lebih sederhana — menjadi sistem kognitif setara dengan **GLM-4** atau **Kimi K2.5**.

## 📦 Instalasi

### Method 1: Workspace Skill (Satu Agent)
```bash
# Copy ke workspace agent Anda
cp -r super-intelligence-skill /path/to/agent-workspace/skills/
```

### Method 2: Managed Skill (Semua Agent di Mesin)
```bash
# Copy ke direktori managed OpenClaw
cp -r super-intelligence-skill ~/.openclaw/skills/super-intelligence-skill
```

### Method 3: Kimi Claw (Browser)
1. Buka Kimi Claw di kimi.com
2. Navigasi ke Skill Workshop
3. Upload folder `super-intelligence-skill`
4. Aktifkan skill

## ⚙️ Konfigurasi (opsional)

Tambahkan ke `openclaw.json` jika ingin mengontrol agent mana yang bisa mengakses:

```json5
{
  agents: {
    defaults: {
      skills: ["super-intelligence-skill"]
    }
  }
}
```

## 🎯 Cara Kerja

Skill ini bekerja dengan **menginjeksi framework kognitif canggih** ke dalam reasoning agent:

1. **Deep Reasoning Mode (DRM)** — Memaksa agent untuk tidak menjawab permukaan
2. **Tree of Thoughts** — Eksplorasi multi-jalur untuk problem-solving
3. **Chain of Verification** — Faktualitas melalui verifikasi berulang
4. **Self-Correction Loops** — Deteksi dan perbaikan error otomatis
5. **Context Management** — Optimasi memori kerja seperti model 2M+ token

## 📁 Struktur File

```
super-intelligence-skill/
├── SKILL.md                           # Entry point & quick start
├── references/
│   ├── reasoning-frameworks.md        # 8 framework berpikir canggih
│   ├── cognitive-patterns.md          # 12 pola kognitif frontier model
│   ├── self-correction.md             # 10 protokol koreksi diri
│   └── context-management.md          # 10 teknik manajemen konteks
└── README.md                          # File ini
```

## 🔥 Hasil yang Diharapkan

Setelah mengaktifkan skill ini, agent Anda akan menunjukkan:

- ✅ **Reasoning depth** yang jauh lebih dalam
- ✅ **Self-correction** aktif sebelum memberikan jawaban
- ✅ **Multi-step planning** yang terstruktur
- ✅ **Error recovery** yang robust
- ✅ **Output quality** setara frontier model
- ✅ **Context handling** yang efisien meski model dasar terbatas

## ⚠️ Catatan Penting

- Skill ini **tidak mengubah model dasar** — ia mengoptimalkan cara model berpikir
- Token usage akan **sedikit lebih tinggi** karena reasoning yang lebih dalam
- Untuk hasil terbaik, gunakan dengan model yang mendukung **tool use** dan **long context**
- Skill ini paling efektif untuk: coding, analysis, research, planning, problem-solving

## 📝 Lisensi

Open Source — bebas digunakan, dimodifikasi, dan didistribusikan.

---

**Dibuat untuk komunitas OpenClaw & Kimi Claw** 🚀
