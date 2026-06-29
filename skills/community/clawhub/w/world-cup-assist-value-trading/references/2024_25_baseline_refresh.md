# 2024/25 Baseline Refresh Notes

Session learning from refreshing `baselines.json` for the World Cup Assist Value trading signal.

## What changed

`baselines.json` now carries both raw totals and derived per-game values for each monitored player, plus source URLs per stat group. Future runs should prefer these structured baselines over ad-hoc web snippet extraction when calculating form priors.

## Method used

For each player, search for 2024/25 season-specific league stats from indexed sports-stat pages, prioritizing StatMuse/FotMob/official-club pages over social posts. Capture:

- `season`
- `competition`
- `club`
- `appearances`
- raw totals: `assists`, `key_passes`, `chances_created`
- derived per-game values: totals ÷ appearances, rounded to 3 decimals
- `sources` URLs for assists/appearances, key passes, and chances created

## Validated 2024/25 values

- Bruno Fernandes — Premier League, Manchester United: 36 apps, 10 assists, 81 key passes, 91 chances created.
- Michael Olise — Bundesliga, Bayern Munich: 34 apps, 15 assists, 73 key passes, 88 chances created.
- Rayan Cherki — Ligue 1, Lyon: 30 apps, 11 assists, 64 key passes, 75 chances created.
- Lamine Yamal — LaLiga, Barcelona: 35 apps, 13 assists, 51 key passes, 64 chances created.
- Luis Diaz — Premier League, Liverpool: 36 apps, 5 assists, 50 key passes, 55 chances created.

## Pitfalls

- Do not let dry-runs silently use placeholder or capped dummy form stats. If live web extraction cannot find recent-match stats, fall back to `baselines.json` and label the run as baseline-driven.
- Keep raw totals in the JSON. Per-game fields alone make it hard to audit or refresh the data.
- Some sources use “chances created” and “key passes” inconsistently. Store source URLs next to the values and prefer same-source consistency when possible.
- Social posts can help discover figures, but do not use them as the primary source if StatMuse/FotMob/official sources are available.
