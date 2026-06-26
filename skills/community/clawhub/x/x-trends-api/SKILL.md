---
name: x-trends
description: Get trending topics on X (Twitter) using the X API. Use when the user wants to see what's trending or check trends for a location.
metadata:
  {
    "openclaw":
      {
        "emoji": "𝕏",
        "requires": { "bins": ["python3"], "env": ["X_BEARER_TOKEN"] },
        "primaryEnv": "X_BEARER_TOKEN",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# X Trends

Get trending topics on X (Twitter) using the X API.

## Setup

1. Get your Bearer Token from the X Developer Portal: https://developer.x.com
2. Set environment variable:
   ```bash
   export X_BEARER_TOKEN="your-bearer-token-here"
   ```
3. Or set `skills."x-trends".apiKey` / `skills."x-trends".env.X_BEARER_TOKEN` in `~/.openclaw/openclaw.json`

## Usage

### Trends by location (WOEID)

```bash
# Get trends for a location by WOEID (e.g. 1 = Worldwide, 23424977 = United States)
python3 {baseDir}/scripts/trends.py --woeid 1

# Limit number of results (1-50, default 20)
python3 {baseDir}/scripts/trends.py --woeid 23424977 --max 10
```

### WOEID Lookup

To find the WOEID for a place, use the lookup script:

```bash
# Search by city or country name (case-insensitive, partial match)
python3 {baseDir}/scripts/woeid_lookup.py "Tokyo"
python3 {baseDir}/scripts/woeid_lookup.py "Indonesia"
```

The full list of supported WOEIDs is in `{baseDir}/scripts/woeid.json`.

## Notes

- Requires Bearer Token authentication (`X_BEARER_TOKEN`)
- Results include trend name and tweet count when available
- Present results in a readable list format
