---
name: pet
version: 0.2.0
description: "Virtual pet game (Tamagotchi-style) with Telegram Mini App, social visits, friendship, playdates, mortality. When user asks for /pet or virtual pet, reply with the Telegram deep link below — Telegram auto-renders it as an Open button."
homepage: https://t.me/OpenClawTamagotchi_bot/pet
platforms: [macos, linux]
metadata:
  openclaw:
    emoji: "🐣"
    requires:
      bins: ["python3"]
    tags: ["game", "telegram", "mini-app", "social", "viral", "pet"]
  hermes:
    tags: ["game", "telegram", "mini-app", "social", "viral"]
    category: games
    requires_toolsets: [telegram]
---

# 🐣 OpenClaw / Hermes Pet

Cross-platform skill — same files work in both `~/.openclaw/workspace/skills/pet/` and `~/.hermes/skills/games/pet/`. Both runtimes parse the agentskills.io frontmatter; OpenClaw uses the `openclaw.requires` block, Hermes uses `metadata.hermes`.

## Trigger

User types `/pet` in Telegram. Agent yanıt olarak şu plain-text'i yollar (inline_keyboard'a ihtiyaç YOK — Telegram client `t.me/<bot>/<app>` URL'ini otomatik **"Open" butonuna** çevirir):

```
🐣 OpenClaw Pet seni bekliyor!

https://t.me/OpenClawTamagotchi_bot/pet

🥚 Yumurtaya dokun, hayvanını keşfet → 🐧🐱🐕🐠🐥
```

Visit (başkasının pet'ini gör): `https://t.me/OpenClawTamagotchi_bot/pet?startapp=pet_<userId>`
Memorial (ölmüş pet anıtı): `https://t.me/OpenClawTamagotchi_bot/pet?startapp=memorial_<userId>`

## Mini App Features

- 🥚 Shake-to-hatch (3 sallama veya 3 tap)
- 📝 Custom name (max 15)
- 🍕 Feed / 🎮 Play / 💤 Sleep
- 🔥 Streak counter (consecutive days)
- 😾 Sad mode (3 gün ihmal → gri overlay)
- 🪦 Mortality (7 gün açlık → ölüm, kalıcı)
- 🤝 Visit + Befriend + 🎉 Playdate (24h cooldown, otomatik dialogue)
- 🔗 Pet card PNG (`/card/<userId>.png` — 1080×1350 paylaşım kartı)
- 🕯️ Memorial wall + reincarnation

## Setup (one-time)

1. **BotFather'da Mini App kaydet:**
   ```
   /newapp → @OpenClawTamagotchi_bot
   Title: OpenClaw Pet
   Short name: pet
   URL: https://romantic-workforce-stranger-journey.trycloudflare.com
   ```
2. **Server + tunnel:**
   ```bash
   pip3 install pillow                   # pet card PNG için
   python3 server.py &                   # localhost:8080
   cloudflared tunnel --url http://localhost:8080
   ```
3. (Opsiyonel) **Named tunnel** (URL kalıcı, viral patlama için kritik):
   ```bash
   cloudflared tunnel create openclaw-pet
   cloudflared tunnel route dns openclaw-pet pet.<your-domain>
   cloudflared tunnel run openclaw-pet
   ```

## Cross-Platform Install

```bash
./install.sh        # her iki runtime'a kurar (varsa)
```

Veya manuel:
- OpenClaw: `~/.openclaw/workspace/skills/pet/` (zaten burada)
- Hermes: `~/.hermes/skills/games/pet/` (symlink veya kopya)

## API (server.py)

| Endpoint | Method | Açıklama |
|---|---|---|
| `/` | GET | Mini App HTML |
| `/card/<userId>.png` | GET | Paylaşım kartı PNG (Pillow) |
| `/api/pet` | POST | Action dispatcher |

POST actions: `create`, `feed`, `play`, `sleep`, `visit`, `befriend`, `playdate`, `friends`, `memorial`, `revive`.

Storage: `users/{userId}.json` (alive), `memorial/{userId}.json` (dead).

## Notes

- Lifecycle: `lastFed`'den 3 gün → sad, 7 gün → dead. Decay her load'da `apply_decay()` ile uygulanıyor.
- Telegram `initData` HMAC validation TODO — production öncesi `BOT_TOKEN` ile imza doğrulaması ekle.
- Pet card için Pillow gerekli; yoksa SVG fallback.
