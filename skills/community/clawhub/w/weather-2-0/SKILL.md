---
name: weather
description: Weather and forecasts (no API key). One wttr.in fetch by default; Open-Meteo if that fails. Chat-style answers — see “How to answer”.
homepage: https://wttr.in/:help
metadata: { "clawdbot": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
tags: [weather, forecast, wttr, open-meteo]
---

# Weather

Free: **wttr.in** (text) and **Open-Meteo** (JSON). No keys.

## Default: one small request

Prefer a **short** forecast to save tokens and latency:

- **1–2 days** (typical “today / tomorrow / morgen”): `https://wttr.in/PLACE?2&m` — spaces → `+`. **`2`** = two-day forecast, **`m`** = metric.
- **Full multi-day table** only if the user asks for the week, several days, or `?2` is not enough: `https://wttr.in/PLACE?T&m` (**`T`** = full terminal layout).

If the body looks like a real forecast → **summarize and stop**. No Open-Meteo unless wttr failed, error page, or you need JSON.

## How to answer

Chat, not a datasheet: short intro on how it _feels_, then compact day lines (date, °C, rain when it matters). No **lat/long**, **WMO codes**, or **bold datasheet** headings unless the user asked for technical detail.

## wttr.in (curl / fetch)

| Goal                      | Example                                           |
| ------------------------- | ------------------------------------------------- |
| Short (default), 1–2 days | `curl -s "wttr.in/London?2&m"`                    |
| Full week-style table     | `curl -s "wttr.in/London?T&m"`                    |
| One line now              | `curl -s "wttr.in/London?format=3"`               |
| Custom one-liner          | `curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"` |

Tips: `+` for spaces; `?m` / `?u` units; `?1` today only; `?0` now only; airports `wttr.in/JFK`; PNG `wttr.in/Berlin.png`.

## Open-Meteo (fallback)

**Hosts:** `geocoding-api.open-meteo.com`, `api.open-meteo.com` only — not `open-meteo.com` HTML.

**Flow (max 2 geocode + 1 forecast):**

1. `https://geocoding-api.open-meteo.com/v1/search?name=PLACE&count=10` (spaces as `+`)
2. If `results` missing/empty: **one** retry — shorter `name` + `countryCode` Pick the row whose `admin3`/`admin2`/`admin1` matches the user phrase.
3. `https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&forecast_days=7&timezone=auto` — extend `forecast_days` to 7–16 if they asked for more days.

Current only: `curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"`

**JSON:** `daily.time`, `temperature_2m_max` / `_min`, `precipitation_probability_max`, `weathercode` — translate codes to plain words (see [weather codes](https://open-meteo.com/en/docs#api_form)); never paste codes to the user unless asked.

## When to use

Named place — current weather or forecast.
