# Example commands: AI agent radar

```bash
python scripts/twitter_trend_radar.py \
  --topic "AI agent" \
  --days 14 \
  --min-likes 50 \
  --limit 30 \
  --format markdown
```

Stricter phrases:

```bash
python scripts/twitter_trend_radar.py \
  --topic "AI agent" \
  --phrase "just launched" \
  --phrase "introducing" \
  --phrase "built this" \
  --min-likes 100
```
