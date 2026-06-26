---
name: zmanim-calculator
slug: jewish-zmanim
version: 1.0.0
description: |
  Calculate Halachic times (zmanim) for any location and date.
  Sunrise, sunset, dawn, dusk, candle lighting, Shabbos times, Daf Yomi,
  and all major zmanim. Uses Hebcal or NOAA algorithms.
  Use when: user asks for Shabbos times, candle lighting, minyan times,
  sunrise/sunset, or any Jewish calendar calculation.
triggers:
  - zmanim
  - shabbos times
  - candle lighting
  - sunrise
  - sunset
  - minyan
  - daf yomi
  - halachic times
  - jewish calendar
metadata:
  openclaw:
    emoji: 🕯️
    requires:
      bins: [python3, pip3]
---

# Zmanim Calculator

Calculate Halachic times for any location and date. Powered by the `hebcal` Python library and NOAA sunrise/sunset algorithms.

## Quick Start

```bash
# Today's zmanim for current location (auto-detected IP)
zmanim today

# Shabbos times for a specific city
zmanim shabbos --city "New York, NY"

# Full zmanim table for a date
zmanim --date 2026-05-15 --lat 40.7128 --lon -74.0060

# Candle lighting time
zmanim candles --city "Jerusalem"

# Daf Yomi for today
zmanim daf

# Weekly parsha
zmanim parsha
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `zmanim today` | All zmanim for today | `zmanim today` |
| `zmanim shabbos` | Shabbos entry/exit times | `zmanim shabbos --city "Brooklyn, NY"` |
| `zmanim candles` | Candle lighting time | `zmanim candles --zip 11230` |
| `zmanim --date YYYY-MM-DD` | Zmanim for specific date | `zmanim --date 2026-06-01` |
| `zmanim --lat X --lon Y` | Zmanim for coordinates | `zmanim --lat 31.7683 --lon 35.2137` |
| `zmanim daf` | Today's Daf Yomi | `zmanim daf` |
| `zmanim parsha` | This week's parsha | `zmanim parsha` |
| `zmanim yomtov` | Upcoming Yom Tov dates | `zmanim yomtov` |

## Output Format

```
📅 Zmanim for Brooklyn, NY — Friday, May 15, 2026
───────────────────────────────────────────────
🕯️ Candle Lighting (18 min):  7:42 PM
🌅 Shkiah (Sunset):           8:02 PM
🌙 Tzeis (72 min):            9:14 PM
🌄 Dawn (Alos HaShachar):     4:12 AM
☀️ Netz HaChamah (Sunrise):   5:42 AM
📖 Sof Zman Shema (Gra):      9:24 AM
📖 Sof Zman Shema (M'A):      8:48 AM
🕰️ Chatzos (Midday):          12:52 PM
🕰️ Mincha Gedolah:           1:12 PM
🕰️ Mincha Ketanah:           4:52 PM
🕰️ Plag HaMincha:            6:27 PM
🌅 Shkiah:                    8:02 PM
```

## Installation

```bash
pip3 install hebcal-python python-dateutil
```

Or use the bundled script (no dependencies):
```bash
python3 scripts/zmanim.py --city "New York, NY"
```

## API

```python
from scripts.zmanim import get_zmanim, get_shabbos_times, get_daf_yomi

# Get all zmanim for a location
times = get_zmanim(lat=40.7128, lon=-74.0060, date="2026-05-15")
print(times['candle_lighting'])

# Shabbos times
shabbos = get_shabbos_times(city="Brooklyn, NY")
print(f"Candles: {shabbos['candle_lighting']}")
print(f"Havdalah: {shabbos['tzeis_72']}")

# Daf Yomi
daf = get_daf_yomi()
print(f"Today: {daf['tractate']} {daf['daf']}")
```

## Configuration

Create `~/.config/zmanim/default.json`:
```json
{
  "default_city": "Brooklyn, NY",
  "candle_lighting_minutes": 18,
  "tzeis_minutes": 72,
  "timezone": "America/New_York"
}
```

## Data Sources

- **Hebcal API** — Jewish calendar calculations
- **NOAA** — Sunrise/sunset algorithms
- **GeoNames** — City-to-coordinates lookup

## Limitations

- Location lookup requires internet (or cached coordinates)
- Extreme latitudes (near poles) may have edge cases
- Yom Tov dates use Hebrew calendar; verify against local minhag
