---
name: ramadan-times
description: Intelligent Ramadan times skill that auto-detects location, provides accurate iftar/sahur times in user's language, and supports 100+ cities worldwide. Supports Turkish, English, Arabic and more.
triggers:
  - ramazan
  - iftar
  - sahur
  - oruç
  - ramadan
  - prayer times
  - iftar saati
  - when is iftar
  - sahur time
metadata:
  openclaw:
    emoji: "🌙"
    requires:
      bins: ["curl", "date"]
    settings:
      location: auto-detect
      language: auto-detect
---

# Ramadan Times Skill 🌙

Intelligent Ramadan times with auto-location detection and multi-language support.

## Features

- 🌍 Auto-detects user location/timezone
- 🌍 Supports 100+ cities worldwide
- 🗣️ Multi-language: TR, EN, AR, DE, FR, ES, RU
- ⏰ Real-time countdown to iftar
- 📅 Weekly schedule support
- 🔔 Daily reminder capability

## Usage

Just ask naturally:
- "İftar saatleri?" / "When is iftar?"
- "Sahur ne zaman?" / "When is sahur?"
- "Ramazan ne zaman başlıyor?"
- "İstanbul iftar"
- "London iftar time"

## Auto-Detection

1. Check user's timezone from OpenClaw config
2. Fallback to Istanbul if not found
3. Support city override in query

## Supported Languages

| Code | Language |
|------|----------|
| tr | Türkçe |
| en | English |
| ar | العربية |
| de | Deutsch |
| fr | Français |
| es | Español |
| ru | Русский |

## Response Examples

### Turkish (auto)
```
🌙 RAMADAN - İstanbul

📅 20 Şubat 2026, Cuma

🌅 Sahur: 04:30
🌅 İftar: 18:47

⏰ İftara: 5 saat 23 dakika
```

### English (auto)
```
🌙 RAMADAN - Istanbul

📅 Friday, February 20, 2026

🌅 Sahur: 04:30
🌅 Iftar: 18:47

⏰ Time until iftar: 5 hours 23 minutes
```

## Supported Cities

Major cities:
- Istanbul, Ankara, Izmir, Istanbul (TR)
- London, New York, Los Angeles, Dubai, Cairo
- Paris, Berlin, Moscow, Tokyo
- And 100+ more...

## API Sources

1. sunrise-sunset.org (sunrise/sunset times)
2. Prayer times API (fallback)
3. Manual calculation (emergency fallback)

## Intelligent Features

1. **Auto-language**: Detect from user or use English
2. **Auto-location**: Get from system timezone
3. **City search**: Override with explicit city name
4. **Time until**: Calculate and show countdown
5. **Next week**: Show entire week's schedule

## Cron Integration

Can be used for daily iftar reminder:
```
0 17 * * * - "İftara 2 saat kaldı!" reminder
```
