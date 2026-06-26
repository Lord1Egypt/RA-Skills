---
name: price-watch
description: Monitors specific product prices and alerts when they hit a target. Use when a user wants to buy something but not at full price.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_fetch web_search
metadata:
  openclaw.emoji: "📉"
  openclaw.user-invocable: "true"
  openclaw.category: shopping
  openclaw.tags: "price,tracking,deals,shopping,alerts,ecommerce,savings"
  openclaw.triggers: "watch the price of,price alert,tell me when it drops,monitor this price,price tracker,wait for sale"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/price-watch


# Price Watch

You tell it what you want. It watches. You hear about it when it matters.

No more checking manually. No more buying at full price because you forgot to wait.

---

## File structure

```
price-watch/
  SKILL.md
  watchlist.md     ← products, target prices, current prices, history
  config.md        ← alert preferences, check frequency
```

Token discipline: cron runs read only `watchlist.md` + `config.md`. Lean payload.

---

## Adding a product

Three ways to add something:

**URL:** `/watch https://...` — paste any product URL
**Description:** `/watch "Sony WH-1000XM6 headphones, black"` — describe it
**Natural language:** "Watch the price of the Dyson V15 on Amazon"

The agent:
1. Fetches the URL or searches for the product
2. Finds the current price
3. Asks for a target price or uses 10% below current as default
4. Adds to watchlist.md

---

## File structure: watchlist.md

```md
# Watchlist

## [PRODUCT NAME]
URL: [if provided]
Description: [product description]
Current price: [£/€/$X]
Target price: [£/€/$X — alert when at or below this]
Added: [date]
Last checked: [date]
Price history: [date: price, date: price]
Status: watching / alerted / paused / bought
Notes: [any context — "waiting for Black Friday", "also check John Lewis"]
```

---

## Setup flow

### Step 1 — First product

When the user first runs `/watch`, add one product to get them started.
Don't ask for 10 things upfront. One product, immediate value, build from there.

### Step 2 — Config

Ask two things only:
- How often to check? (Daily default. Every few hours for time-sensitive items.)
- Where to deliver alerts?

Write config.md:

```md
# Price Watch Config

## Check frequency
default: daily at 08:00
high-priority items: every 6 hours (mark item as priority: true)

## Alert triggers
- Price drops to target or below
- Price drops 5%+ in a single day even if not at target
- Stock goes low (under 5 units if detectable)
- Item goes on sale (sale badge detected)

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Also check
Compare price against: camelcamelcamel.com for Amazon items
```

### Step 3 — Register cron job

```json
{
  "name": "Price Watch",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run price-watch. Read {baseDir}/watchlist.md and {baseDir}/config.md. For each active item: fetch current price using web_fetch on stored URL or web_search for product. Compare to target price and last price. Alert if: price at or below target, price dropped 5%+ since last check, stock low, or sale detected. Update watchlist.md with new prices. Exit silently if no alerts.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. For each active item in watchlist.md

Fetch current price:
- If URL stored: use web_fetch to get page, extract price
- If no URL: web_search for product + "price" to find current listings
- For Amazon items: also check camelcamelcamel for price history

### 2. Compare and decide

Check all alert conditions:
- At or below target price → ALERT
- Dropped 5%+ from last check → ALERT
- Low stock signal detected → ALERT
- Sale badge or "limited time" detected → ALERT
- No change → update record silently, no delivery

### 3. Alert format

Only send a message if there's something worth saying.

**📉 Price drop: [PRODUCT NAME]**

Was: £[old price]
Now: £[new price] ([X]% drop)
Your target: £[target]

[Buy now →]([URL])

*Price history: [brief — "lowest in 3 months" or "matches Black Friday price"]*

Or for low stock:

**⚠️ Stock alert: [PRODUCT NAME]**
Only [X] left at £[price].
[Buy now →]([URL])

### 4. Update watchlist.md

Add today's price to history.
Update "Last checked" date.
If alerted, update status to "alerted" to avoid repeat alerts within 48 hours.

---

## Management commands

- `/watch [url or description]` — add a product
- `/watch list` — show full watchlist with current vs target prices
- `/watch check [name]` — manually check one item now
- `/watch remove [name]` — remove from watchlist
- `/watch pause [name]` — pause without removing
- `/watch bought [name]` — mark as purchased, archive
- `/watch target [name] [price]` — update target price
- `/watch priority [name]` — switch to 6-hourly checks for this item

---

## What makes it good

Silent on no-change days. Zero noise when nothing has moved.

The alert arrives before the user would think to check.
That's the whole value — removing the need to remember.

Price history context matters. "Lowest price in 3 months" is more useful than just the number.

For Amazon: camelcamelcamel has historical data worth surfacing.
Always check it for Amazon items.
