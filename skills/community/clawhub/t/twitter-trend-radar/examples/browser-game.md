# Example commands: browser game radar

```bash
python scripts/twitter_trend_radar.py \
  --topic "browser game" \
  --days 30 \
  --min-likes 20 \
  --limit 30 \
  --max-queries 8 \
  --format markdown \
  --output reports/browser-game-radar.md
```

With Chrome profile:

```bash
python scripts/twitter_trend_radar.py \
  --topic "browser game" \
  --days 30 \
  --min-likes 20 \
  --bird-arg "--chrome-profile" \
  --bird-arg "Default"
```
