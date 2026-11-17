# twitter-trend-radar

A read-only agent skill for finding early opportunities on X/Twitter using the local `bird` CLI.

## Install into a skills folder

Copy this folder into your agent/Claude/OpenClaw skills directory, for example:

```bash
cp -R twitter-trend-radar ~/.claude/skills/twitter-trend-radar
```

## Quick test

```bash
cd ~/.claude/skills/twitter-trend-radar
python scripts/twitter_trend_radar.py --topic "browser game" --days 30 --min-likes 20 --dry-run
```

Then remove `--dry-run` after bird is configured.
