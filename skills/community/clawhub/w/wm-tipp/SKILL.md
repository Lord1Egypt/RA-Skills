---
name: wm-tipp
description: "WM 2026 Tipps mit Polymarket-Quoten. Automatische Daily-Tipps an Telegram."
version: 1.0.1
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - WM_CHAT_IDS
        - WM_TELEGRAM_API
      bins:
        - python3
---

# WM 2026 Tipps – Skill

> Automatische WM-Tipps mit Polymarket-Quoten. Täglich 18:00 MESZ.

## Features
- Liest Spielplan aus JSON
- Holt Live-Quoten von Polymarket (public API, kein Key nötig)
- 1h-Cache für Polymarket-Daten
- Sendet Tipps an konfigurierbare Telegram-Empfänger
- Markdown-Format für Telegram

## Installation

```bash
clawhub install wm-tipp
```

## Konfiguration

**Environment-Variablen** (setzen vor dem Script):

```bash
# Telegram Gateway Endpoint
export WM_TELEGRAM_API="http://localhost:8080/api/telegram/send"

# Empfänger als JSON-Array
export WM_CHAT_IDS='[{"name": "Alice", "chat_id": "123456789"}, {"name": "Bob", "chat_id": "987654321"}]'
```

**Beispiel-Cron:**

```bash
# Täglich um 18:00 MESZ (16:00 UTC)
0 16 * * * WM_TELEGRAM_API=http://localhost:8080/api/telegram/send WM_CHAT_IDS='[{"name":"Du","chat_id":"DEINE_ID"}]' /usr/bin/python3 /home/HolBot/skills/wm-tipp/scripts/wm_tipps.py >> /tmp/wm_tipp.log 2>&1
```

## Spielplan anpassen

`data/wm2026_schedule.json` bearbeiten:

```json
{
  "games": [
    {
      "date": "2026-06-11",
      "time_mesz": "21:00",
      "team1": "Mexiko",
      "team2": "Südafrika",
      "stadium": "Estadio Azteca",
      "group": "A",
      "stage": "Gruppenphase"
    }
  ]
}
```

## Tipps anpassen

In `scripts/wm_tipps.py` das `TIPS`-Dictionary bearbeiten:

```python
TIPS = {
    ("Deutschland", "Curaçao"): {"tipp": "4:0", "reason": "..."},
}
```

## Polymarket

- **Öffentliche API** – kein API-Key nötig
- **Endpoint:** `https://gamma-api.polymarket.com/markets`
- **Cache:** `data/polymarket_cache.json` (1h TTL)

## Dateien

```
wm-tipp/
├── SKILL.md
├── scripts/
│   └── wm_tipps.py           # Hauptscript
└── data/
    ├── wm2026_schedule.json  # Spielplan
    ├── wm_tipps.json         # Gespielte Tipps
    └── polymarket_cache.json  # Polymarket-Cache
```

## Requirements
- Python 3.8+
- Telegram-Bot via OpenClaw Gateway
- Internet-Zugriff für Polymarket-API

---

*Kein API-Key nötig. Spielplan und Tipps einfach anpassen.*