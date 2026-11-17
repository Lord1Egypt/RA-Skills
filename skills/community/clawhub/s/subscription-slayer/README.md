# Subscription Slayer ⚔️

Find and slay the subscriptions draining your wallet every month.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

People forget about subscriptions and waste money on unused services. The average person has 10+ subscriptions and underestimates their total spend by 2.5×. Auto-renewing charges silently drain accounts month after month.

## The Solution

**Subscription Slayer** analyzes your subscriptions to:
1. **Calculate** exact monthly and annual costs
2. **Detect** which subscriptions are likely unused (waste detection scoring)
3. **Rank** everything by waste probability
4. **Generate** ready-to-send cancellation email templates

## Quick Start

```bash
# Analyze your subscriptions
python3 scripts/subscription_tracker.py analyze my_subs.json

# Get JSON output
python3 scripts/subscription_tracker.py analyze my_subs.json --json

# Generate a cancellation email for a specific subscription
python3 scripts/subscription_tracker.py cancel my_subs.json --name "Netflix"

# Generate cancellation emails for all high-waste subscriptions
python3 scripts/subscription_tracker.py cancel my_subs.json --threshold 70

# Run the demo with sample data
python3 scripts/subscription_tracker.py demo
```

## Subscription JSON Format

Create a JSON file with your subscriptions:

```json
[
  {
    "name": "Netflix",
    "cost": 15.49,
    "billing_cycle": "monthly",
    "category": "streaming",
    "last_used": "2024-01-15",
    "start_date": "2022-03-01",
    "auto_renew": true,
    "cancel_url": "https://www.netflix.com/cancelplan"
  }
]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Subscription name |
| `cost` | ✅ | Cost per billing cycle |
| `billing_cycle` | ✅ | monthly, yearly, weekly, quarterly |
| `category` | ❌ | streaming, software, fitness, etc. |
| `last_used` | ❌ | ISO date of last use |
| `start_date` | ❌ | When subscription started |
| `auto_renew` | ❌ | Auto-renew status (default true) |
| `cancel_url` | ❌ | URL to manage subscription |

## Waste Detection

The waste score (0–100) uses 5 factors:

| Factor | Weight | What it measures |
|--------|--------|------------------|
| Days since last use | 40% | How long since you used the service |
| Cost vs. usage | 25% | Expensive + unused = high waste |
| Subscription age | 15% | Old subs are easily forgotten |
| Auto-renew status | 10% | Silent renewals drain money |
| Category tendency | 10% | Some categories are more forgettable |

**Score interpretation:**
- 🔴 **80–100**: Critical — cancel now
- 🟠 **60–79**: High — likely unused
- 🟡 **40–59**: Moderate — review
- 🟢 **0–39**: Low — probably in use

See `references/waste_detection.md` for the full methodology.

## Example Output

```
============================================================
  ⚔️  SUBSCRIPTION SLAYER
============================================================

  Total monthly cost:   $276.42/mo
  Total annual cost:    $3,317.04/yr
  Active subscriptions: 10

  💸 Potential annual savings: $1,559.76
     (by cancelling 5 high-waste subscriptions)

  📊 SUBSCRIPTIONS RANKED BY WASTE
  --------------------------------------------------------
   1. Adobe Creative Cloud
      🟠 High — likely unused
      Waste: [████████████████░░░░] 80/100
      $54.99/mo  ($659.88/yr)  Category: software  426d unused

  ...

  ⚔️  RECOMMENDATION: Cancel these now
  --------------------------------------------------------
     • Adobe Creative Cloud  —  save $659.88/yr
     • NYT Digital           —  save $204.00/yr
     • Dropbox Plus          —  save $143.88/yr
```

## Features

- **Multi-factor waste detection** — 5-factor scoring algorithm
- **All billing cycles** — weekly, monthly, quarterly, yearly, and more
- **Category analysis** — see spending by category
- **Cancellation emails** — formal, ready-to-send templates
- **Savings calculator** — see exactly how much you'd save by cancelling
- **Demo mode** — 10 sample subscriptions show the full workflow
- **Stdlib only** — no pip installs, runs on any Python 3.10+

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill definition and agent workflow |
| `scripts/subscription_tracker.py` | Main analysis and email generation script |
| `references/waste_detection.md` | Scoring methodology documentation |
| `references/cancellation_template.md` | Email template reference |

## License

MIT © Denis Voronin
