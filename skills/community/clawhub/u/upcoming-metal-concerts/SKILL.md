---
name: upcoming-metal-concerts
description: Collect upcoming metal concerts and festivals by country using concerts-metal.com. Use when the user asks about upcoming metal shows, gigs, or festivals.
metadata: {"openclaw":{"emoji":"🤘","requires":{"bins":["python3"]}}}
---

# Upcoming Metal Concerts

Collect upcoming metal concerts and festivals worldwide via concerts-metal.com.

## First run

On first run, `skill-config.json` is created with default settings. **The default country is Spain (ES).** Tell the user this and ask them which country they'd like to use. To see all supported country codes, run:

```bash
python3 {baseDir}/scripts/events.py --list-countries
```

Then update `country` in `{baseDir}/skill-config.json` to the user's chosen code before collecting.

## Usage

Run the collector to scrape and accumulate concert data into `data/concerts.json`:

```bash
python3 {baseDir}/scripts/events.py
```

The `--country` flag overrides the config for a single run without changing it:

```bash
python3 {baseDir}/scripts/events.py --country DE
```

Re-running merges new concerts without duplicates and flags previously-seen future concerts that disappear from the source as potentially cancelled. Each record contains `date`, `artists`, `venue`, `city`, `url`, `discovered_at`, and `status` (`"active"` or `"cancelled"`).

## Changing settings

All settings live in `{baseDir}/skill-config.json`:

```json
{
  "country": "ES",
  "concert_days": 200
}
```

| Key | What it does | How to change |
|-----|-------------|---------------|
| `country` | ISO country code to scrape. | Set to any code from `--list-countries` (e.g. `"DE"`, `"US"`, `"GB"`). |
| `concert_days` | How many days ahead to look for concerts. | Set to any positive integer (e.g. `90` for ~3 months, `365` for a year). |

When the user asks to change their country or lookahead window, edit the relevant key in `{baseDir}/skill-config.json` directly.

## Data files

All data lives in `data/` (gitignored):
- `concerts.json` — accumulated concert records

## Notes

- No API key required. Data is sourced from concerts-metal.com broadcast pages.
- Coverage is excellent for metal, punk, hardcore, and adjacent genres across 50+ countries.
