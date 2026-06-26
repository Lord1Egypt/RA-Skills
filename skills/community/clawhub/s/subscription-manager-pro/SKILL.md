---
name: subscription-manager-pro
description: Track all your subscriptions, get alerts before renewals, identify forgotten services, and calculate total spend. Never pay for something you forgot to cancel again.
homepage: https://github.com/openclaw/skills/tree/main/skills/subscription-manager-pro
metadata:
  clawdbot:
    emoji: "💳"
    requires:
      files:
        - "scripts/*"
---

# Subscription Manager Pro 💳

> Stop paying for subscriptions you forgot about. Track everything, get reminded before charges, and reclaim your money.

## Why This Skill?

The average person wastes **$133/month** on forgotten subscriptions (C+R Research, 2022). This skill helps you:

- 📋 **Track** all subscriptions in one place
- ⏰ **Alert** you before renewal dates (configurable)
- 💰 **Calculate** total monthly/yearly spend
- 🔍 **Identify** unused or duplicate services
- 📊 **Analyze** spending patterns and suggest cuts

## Use When

- User mentions "subscriptions", "recurring charges", "monthly bills"
- User asks about Netflix, Spotify, AWS, or any service cost
- User wants to audit their spending
- User says "what am I paying for" or "cancel subscription"
- User wants renewal reminders

## Commands

### Add a Subscription
```
add subscription Netflix $15.99/month renews on the 15th
add sub Spotify $9.99 monthly
add AWS ~$50/month variable
```

### List All Subscriptions
```
show my subscriptions
list subs
what subscriptions do I have?
```

### Check Upcoming Renewals
```
what's renewing soon?
upcoming charges this week
renewals in the next 30 days
```

### Cancel/Remove Subscription
```
remove Netflix subscription
cancel Spotify
mark Hulu as cancelled
```

### Spending Summary
```
how much am I spending on subscriptions?
subscription spending summary
total monthly subscription cost
```

### Mark as Paused/Active
```
pause Netflix subscription
resume Spotify
```

### Find Unused Subscriptions
```
find unused subscriptions
which subscriptions haven't I used lately?
```

## Data Storage

All data stored locally in JSON:
```
~/.openclaw/workspace/subscription-manager-pro/data/
├── subscriptions.json    # All subscription records
├── reminders.json        # Reminder settings
└── history.json          # Payment history log
```

## Subscription Record Format

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
  "last_used": "2026-03-20",
  "created_at": "2026-01-01",
  "remind_days_before": 3
}
```

## Categories

Subscriptions are auto-categorized:
- 🎬 Entertainment (Netflix, Spotify, Disney+, etc.)
- 💻 Software (Adobe, Office 365, etc.)
- ☁️ Cloud/Hosting (AWS, Vercel, etc.)
- 📰 News/Media (NYT, Substack, etc.)
- 🏋️ Health/Fitness (Gym, Peloton, etc.)
- 📚 Education (Coursera, Skillshare, etc.)
- 🔧 Utilities (Phone, Internet, etc.)
- 🛒 Shopping (Amazon Prime, Costco, etc.)
- 🤖 AI/Tools (ChatGPT, Claude, etc.)
- 📦 Other

## Reminder System

Set up proactive reminders:
```
remind me 3 days before any renewal
set Netflix reminder to 7 days
disable reminders for AWS
```

Default: 3 days before renewal

## Scripts

All operations handled by `scripts/manager.py`:

```bash
# Add subscription
python scripts/manager.py add --name "Netflix" --cost 15.99 --cycle monthly --day 15

# List all
python scripts/manager.py list

# Upcoming renewals
python scripts/manager.py upcoming --days 7

# Spending summary
python scripts/manager.py summary

# Remove subscription
python scripts/manager.py remove --name "Netflix"

# Export to CSV
python scripts/manager.py export --format csv
```

## Example Session

**User**: "add my Netflix subscription, $15.99 per month, renews on the 15th"

**Agent**: Added Netflix subscription:
- 💳 Cost: $15.99/month
- 📅 Renews: 15th of each month
- 🏷️ Category: Entertainment
- ⏰ Reminder: 3 days before

**User**: "how much am I spending on subscriptions?"

**Agent**: 📊 **Subscription Summary**

| Category | Monthly | Yearly |
|----------|---------|--------|
| Entertainment | $45.97 | $551.64 |
| Software | $29.99 | $359.88 |
| Cloud/Hosting | $52.00 | $624.00 |
| **Total** | **$127.96** | **$1,535.52** |

💡 You're spending $1,535/year on subscriptions.

**User**: "what's renewing this week?"

**Agent**: ⏰ **Upcoming Renewals (Next 7 Days)**

| Service | Date | Amount |
|---------|------|--------|
| Netflix | Mar 15 | $15.99 |
| Spotify | Mar 17 | $9.99 |

Total upcoming: **$25.98**

## Pro Tips

1. **Add cancel URLs** when you add subscriptions — makes cancelling one click
2. **Track "last used"** to identify zombie subscriptions
3. **Use heartbeat** to get daily renewal alerts
4. **Export monthly** to spreadsheet for records

## Integration with Heartbeat

Add to your `HEARTBEAT.md`:
```markdown
## Subscription Checks
- [ ] Check for renewals in next 3 days
- [ ] Alert if any subscription renewing tomorrow
```

## Privacy

- All data stored locally, never leaves your machine
- No API keys required
- No external services
- Full control over your data
