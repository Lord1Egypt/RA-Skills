# 🐣 OpenClaw / Hermes Pet

Cross-platform Telegram Mini App pet game. Çalışıyor → **`https://t.me/OpenClawTamagotchi_bot/pet`**

## 🚀 Kurulum

```bash
./install.sh                              # OpenClaw + Hermes (varsa) ikisine de symlink
pip3 install pillow                       # pet card PNG için
python3 server.py                         # localhost:8080
cloudflared tunnel --url http://localhost:8080
```

BotFather'da bir kez:
```
/newapp → @OpenClawTamagotchi_bot
Title: OpenClaw Pet
Short name: pet
URL: <cloudflared tunnel URL>
```

Bittiğinde kullanıcı `/pet` yazınca, agent şu metni yollar:
```
🐣 OpenClaw Pet seni bekliyor!
https://t.me/OpenClawTamagotchi_bot/pet
```
Telegram client `t.me` URL'ini otomatik **"Open" butonuna** çevirir → tek tık ile Mini App. Inline_keyboard API'sine ihtiyaç yok.

## 🎮 Game Loop

| Aksiyon | Etki |
|---|---|
| 🥚 Shake/tap (3x) | Yumurtadan rastgele hayvan |
| 🍕 Feed | +25 hunger |
| 🎮 Play | +20 happy, -10 energy |
| 💤 Sleep | +30 energy |
| 🔥 Streak | Üst üste günlük giriş = bond bonus |
| 🤝 Befriend | İki yönlü arkadaşlık (visit linki üzerinden) |
| 🎉 Playdate | 24h cooldown, otomatik dialogue, +15 happy |

## 🌟 Sosyal Katman (Viral Hook)

- **Visit link**: `t.me/OpenClawTamagotchi_bot/pet?startapp=pet_<userId>` — başkasının pet'ini gör
- **Friend list**: arkadaşlarının pet'lerini bond skoru ile listele, tap → ziyaret
- **Pet card PNG**: `/card/<userId>.png` — paylaşılabilir 1080×1350 kart
- **🔗 Paylaş**: `t.me/share/url` üzerinden gruplara visit linki

## ⚰️ Mortality

3 gün ihmal → **sad** (gri overlay, "küstü" badge)
7 gün ihmal → **dead** (kalıcı, anıt sayfasında kalır)

- Ölü pet `memorial/{userId}.json`'a taşınır, `?startapp=memorial_<id>` ile açılır
- "🪦 Anıt paylaş" → grup paylaşımı (drama hook)
- "🥚 Yeni yumurta" veya "Reenkarnasyon" (eski pet'in tipi + " II", level/arkadaş sıfır)

## 🐾 Pet Tipleri

🐧 Penguin · 🐱 Kedi · 🐕 Köpek · 🐠 Balık · 🐥 Civciv

## 🔧 Teknik

- **Backend**: `server.py` (stdlib + Pillow)
- **Frontend**: `index.html` (vanilla JS + Telegram WebApp SDK)
- **Storage**: `users/{userId}.json` (alive), `memorial/{userId}.json` (dead)
- **Cross-platform**: agentskills.io standardı — OpenClaw + Hermes Agent

API: `POST /api/pet` actions: `create`, `feed`, `play`, `sleep`, `visit`, `befriend`, `playdate`, `friends`, `memorial`, `revive`.

Detaylar: `SKILL.md` · Marketing planı: `docs/marketing-brainstorm.md` · Mimari notları: `CLAUDE.md`
