# 2025/26 Baseline Refresh Notes

Session learning from refreshing `baselines.json` from 2024/25 to 2025/26 season data.

## What to update
For each monitored player, keep `baselines.json` structured with:
- `season`, `competition`, `club`
- `appearances`, plus `starts` and `minutes` when available
- raw totals: `assists`, `key_passes`, `chances_created`
- derived per-game fields: `assists_per_game`, `key_passes_per_game`, `chances_created_per_game`
- `sources` URLs for auditability

Validate derived fields after editing:
```bash
python3 -m json.tool /root/.hermes/skills/world-cup-assist-value-trading/baselines.json >/tmp/baselines.validated.json && python3 - <<'PY'
import json
p='/root/.hermes/skills/world-cup-assist-value-trading/baselines.json'
with open(p) as f: data=json.load(f)
for name,v in data.items():
    for total_key, per_key in [('assists','assists_per_game'),('key_passes','key_passes_per_game'),('chances_created','chances_created_per_game')]:
        calc=round(v[total_key]/v['appearances'],3)
        if abs(calc-v[per_key])>0.001:
            raise SystemExit(f'{name} {per_key} mismatch: {v[per_key]} != {calc}')
print('OK: JSON valid and per-game values match totals/appearances for', len(data), 'players')
PY
```

## Source strategy that worked
- Use FotMob player pages for full 2025/26 season snapshots: appearances, starts, minutes, assists, chances created, big chances created, xA.
- Use StatMuse targeted searches for season-level key passes when FotMob extraction omits that field.
- Use FootyStats only when it gives a clear per-game key-passes value; convert to total as `round(key_passes_per_game * appearances)` and keep the source label explicit.
- Prefer direct source pages and indexed snippets over social posts. Social posts can help discover numbers but should not be the primary citation unless no better source exists.

## 2025/26 values captured in latest refresh
- Bruno Fernandes — Manchester United, Premier League: 35 apps, 21 assists, 112 key passes, 136 chances created.
- Michael Olise — Bayern Munich, Bundesliga: 32 apps, 19 assists, 61 key passes, 79 chances created.
- Rayan Cherki — Manchester City, Premier League: 33 apps, 12 assists, 49 key passes, 60 chances created.
- Lamine Yamal — Barcelona, LaLiga: 28 apps, 11 assists, 60 key passes, 72 chances created.
- Luis Diaz — Bayern Munich, Bundesliga: 32 apps, 14 assists, 77 key passes, 65 chances created.

## Pitfalls
- The original script's snippet-summing logic can produce placeholder-like capped values; do not present that as real form unless `baselines.json` or a reliable last-5-match source backs it.
- Current FotMob pages reflect 2025/26 and may differ from older 2024/25 refreshes; always check the requested season explicitly.
- Player clubs changed for 2025/26: Rayan Cherki is Manchester City; Luis Diaz is Bayern Munich; Michael Olise is Bayern Munich.
