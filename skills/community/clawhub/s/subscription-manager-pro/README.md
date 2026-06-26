# Subscription Manager Pro 💳

> **Stop paying for subscriptions you forgot about.** Track everything, get reminded before charges, and reclaim your money.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai/subscription-manager-pro)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## The Problem

The average person wastes **$133/month** on forgotten subscriptions (C+R Research, 2022). That's **$1,596/year** going to services you don't use!

## The Solution

Subscription Manager Pro is an OpenClaw skill that:

- 📋 **Tracks** all your subscriptions in one place
- ⏰ **Alerts** you BEFORE renewal dates (not after)
- 💰 **Calculates** your total monthly/yearly spend
- 🔍 **Identifies** unused or duplicate services
- 📊 **Analyzes** spending patterns by category

## Quick Start

### Install

```bash
clawhub install subscription-manager-pro
```

Or manually copy to `~/.openclaw/workspace/skills/subscription-manager-pro/`

### Usage

Talk naturally to your OpenClaw agent:

```
"Add my Netflix subscription, $15.99 per month"
"What subscriptions do I have?"
"What's renewing this week?"
"How much am I spending on subscriptions?"
"Cancel my Hulu subscription"
```

## Features

### 🎯 Smart Categorization

Auto-detects categories based on service name:
- 🎬 Entertainment (Netflix, Spotify, Disney+)
- 💻 Software (Adobe, Office 365, Notion)
- ☁️ Cloud (AWS, Vercel, DigitalOcean)
- 📰 News (NYT, Substack, Medium)
- 🏋️ Fitness (Gym, Peloton, Headspace)
- 📚 Education (Coursera, Skillshare)
- 🤖 AI/Tools (ChatGPT, Claude, Midjourney)

### 📅 Proactive Reminders

Get notified **before** you're charged:
```
🔴 Netflix renews TOMORROW ($15.99)
🟡 Spotify renews in 3 days ($9.99)
```

### 📊 Spending Insights

```
📊 Subscription Spending Summary

| Category      | Monthly   | Yearly     |
|---------------|-----------|------------|
| 🎬 Entertainment | $45.97    | $551.64    |
| 💻 Software      | $29.99    | $359.88    |
| ☁️ Cloud         | $52.00    | $624.00    |
| **TOTAL**        | **$127.96** | **$1,535.52** |

💡 You're spending $1,535/year on subscriptions!
```

### 🔒 Privacy First

- All data stored **locally** in JSON
- No API keys required
- No external services
- Full control over your data

## CLI Usage

```bash
# Add subscription
python scripts/manager.py add --name "Netflix" --cost 15.99 --cycle monthly --day 15

# List all subscriptions
python scripts/manager.py list

# Show upcoming renewals
python scripts/manager.py upcoming --days 7

# Spending summary
python scripts/manager.py summary

# Cancel subscription
python scripts/manager.py remove --name "Netflix"

# Export to CSV
python scripts/manager.py export --format csv

# Check reminders
python scripts/manager.py reminders
```

## Data Format

Subscriptions are stored in `~/.openclaw/workspace/subscription-manager-pro/data/subscriptions.json`:

```json
{
  "id": "uuid",
  "name": "Netflix",
  "cost": 15.99,
  "currency": "USD",
  "billing_cycle": "monthly",
  "renewal_day": 15,
  "category": "entertainment",
  "status": "active",
  "notes": "4K plan, family sharing",
  "cancel_url": "https://netflix.com/cancelplan",
  "remind_days_before": 3
}
```

## Integration with Heartbeat

Add to your `HEARTBEAT.md` for daily alerts:

```markdown
## Subscription Checks
- [ ] Check for renewals in next 3 days
- [ ] Alert if spending > $150/month
```

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)

## Contributing

PRs welcome! Please follow the [ClawHub skill guidelines](https://clawhub.ai/about/guidelines).

## License

MIT License - see [LICENSE](LICENSE)

---

Made with 💳 for the OpenClaw community
