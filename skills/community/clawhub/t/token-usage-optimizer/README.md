# Token Usage Optimizer

**Maximize your Claude Code subscription value** with smart usage monitoring and burn rate optimization.

## Why?

You're paying **$20-200/month** for Claude Code. This skill helps you:

- 📊 **Track usage** — 5-hour session & 7-day weekly quotas
- ⚡ **Get alerts** — One-time warnings at 50% session usage
- 🎯 **Optimize burn rate** — See if you're under/over/on-pace daily
- 💰 **Maximize value** — Use your subscription to its fullest

## Quick Start

```bash
# 1. Setup tokens
./scripts/setup.sh

# 2. Check usage
./scripts/check-usage.sh

# 3. Daily report
./scripts/report.sh
```

## Features

- ✅ **Burn Rate Tracking** — UNDER/OK/OVER vs ~14%/day budget
- ✅ **Smart Alerts** — One-time warnings (no spam)
- ✅ **Plan-Aware** — Works with Pro, Max 100, Max 200
- ✅ **Ultra-Lightweight** — 10-min cache, minimal API calls
- ✅ **No Dependencies** — Just bash + curl + python3
- ✅ **Manual Refresh** — ~Once per week, 30 seconds (`claude auth login`)

## Output Example

```
📊 Claude Code Daily Check:

⏱️  SESSION (5h): 22%
📅 WEEKLY (7d): 49%

⚪ On pace — optimal usage
```

## Installation

### Via ClawHub (Recommended)

```bash
clawdhub install token-usage-optimizer
```

### Manual

```bash
git clone https://github.com/yourusername/token-usage-optimizer.git
cd token-usage-optimizer
./scripts/setup.sh
```

## Integration with OpenClaw

Add to `HEARTBEAT.md`:

```markdown
### Evening Check (18:00-20:00)
- Claude Code usage: /path/to/token-usage-optimizer/scripts/report.sh
```

## Documentation

- [`SKILL.md`](SKILL.md) — Full skill documentation
- [`references/api-endpoint.md`](references/api-endpoint.md) — API details
- [`references/token-extraction.md`](references/token-extraction.md) — How to get tokens
- [`references/plans.md`](references/plans.md) — Subscription tiers

## Security

- Tokens stored in `.tokens` (gitignored)
- File permissions: 600 (owner read/write only)
- Never commit tokens to git

## License

MIT

## Contributing

Found a bug? Have a feature request?

→ Open an issue on [ClawHub](https://clawhub.ai/friday/token-usage-optimizer)

## Author

Created by Friday (П'ятниця) 🏝️

Built to solve the problem: "I'm paying $100/month but don't know if I'm using it optimally."
