---
name: ecommerce-deal-scout
description: Proactively surfaces deals matching user preferences before they knew to look. Use when a user wants discovery-mode deal finding rather than specific price tracking.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch
metadata:
  openclaw.emoji: "🛍️"
  openclaw.user-invocable: "true"
  openclaw.category: shopping
  openclaw.tags: "deals,shopping,ecommerce,discounts,bargains,offers"
  openclaw.triggers: "find me deals,deal scout,shopping deals,best offers,alert me to deals,looking for deals"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/ecommerce-deal-scout


# Ecommerce Deal Scout

Price Watch is reactive — you tell it what to watch.
Deal Scout is proactive — it finds things you'd want before you knew to look.

Runs daily. Only delivers when something is genuinely worth your attention.

---

## Scope — personal shopping only

This skill surfaces deals for the user's personal purchases based on their
own stated preferences. It is not for:
- Lead generation or competitor price monitoring
- Resale arbitrage or bulk purchasing
- Scraping prices for commercial use

The watchlist and preferences contain only items the user personally wants to buy.

---

## The difference from price-watch

`price-watch` = you found something specific, you want to know when it gets cheaper
`ecommerce-deal-scout` = you have preferences, it surfaces deals you'd want across categories

They work together. Price Watch for specific items. Deal Scout for discovery.

---

## File structure

```
ecommerce-deal-scout/
  SKILL.md
  preferences.md   ← categories, brands, size/spec filters, budget ranges
  history.md       ← deals surfaced, deals acted on, patterns learned
  config.md        ← delivery, frequency, quality bar
```

---

## Setup flow

### Step 1 — Preferences interview

Ask conversationally, not as a form. Cover:

**Categories you shop:**
"What do you actually buy online? Clothes, tech, homeware, books, sports gear, beauty — what are your main categories?"

**Brands you like:**
"Any brands you'd always consider if the price was right?"

**What you avoid:**
"Anything you never buy? Fast fashion, certain platforms, whatever."

**Budget sense:**
"What's your rough threshold for 'that's a good deal' vs 'that's expensive'?"

**Timing:**
"Are there things you're in the market for right now, or is this more about surfacing things when the price is right?"

Don't ask all at once. Have a short conversation. Two or three questions max before writing the file.

### Step 2 — Write preferences.md

```md
# Deal Scout Preferences

## Categories I buy
[category]: [notes — e.g. "mostly basics, neutral colours, size M"]
[category]: [notes]

## Brands I like
[brand]: [why / what I buy from them]
[brand]: [context]

## Never show me
[brands, categories, or types to always skip]

## Budget ranges
[category]: under £[X] is a deal, over £[Y] is too expensive
[category]: [range]

## Currently in market for
[anything specific they mentioned wanting now]

## Quality bar
Only surface genuine deals — 20%+ off or genuinely unusual prices.
Not "10% off" newsletter discounts. Real deals.
```

### Step 3 — Write config.md

```md
# Deal Scout Config

## Scan frequency
Daily at [TIME]

## Max deals per day
3 — quality over quantity. If nothing genuinely good: silent.

## Delivery
channel: [CHANNEL]
to: [TARGET]

## Sources to scan
web_search: true
Check: brand sites, aggregators (hotukdeals, camelcamelcamel for Amazon)
```

### Step 4 — Register cron job

```json
{
  "name": "Ecommerce Deal Scout",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "<USER_TIMEZONE>" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run ecommerce-deal-scout. Read {baseDir}/preferences.md, {baseDir}/history.md, and {baseDir}/config.md. Search for genuine deals matching the user's preferences. Only surface deals that are: 20%+ off, unusually low price for that item, or match 'currently in market for' list. Max 3 deals. If nothing genuinely good: exit silently. Update history.md with what was surfaced.",
    "lightContext": true
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL>", "to": "<TARGET>", "bestEffort": true }
}
```

---

## Runtime flow

### 1. Read preferences

Load categories, brands, budget ranges, current wishlist.
Check history.md — what was recently surfaced to avoid repeats.

### 2. Scan for deals

For each preference category, run targeted web_search:
- "[brand] sale", "[category] deal today", "[item] price drop"
- Check deal aggregator sites for the user's categories
- Check brand sites directly for sale sections

Quality filter — only keep if:
- Genuinely 20%+ off regular price (verify this — don't trust "was/now" on the page)
- Or matches "currently in market for" at any reasonable price
- Or unusual find the user would likely not encounter themselves

Discard:
- Newsletter "10% off your next order" type deals
- Items not matching preferences
- Anything surfaced in the last 7 days (check history.md)

### 3. Rank and pick top 3

If more than 3 pass the quality filter, pick the best:
- Highest relevance to preferences
- Best actual savings
- Most time-sensitive (limited stock / flash sale)

If fewer than 3 genuinely good deals: deliver what's real. If nothing passes: silent exit.

### 4. Format output

**🛍️ Deal Scout — [DATE]**

---

**[ITEM NAME]** — [brand] — £[NOW] ~~£[WAS]~~ ([X]% off)
[One sentence: why this is a genuine deal and why it fits the user's preferences]
[Link]
⏱ [urgency signal if relevant — "sale ends tonight", "only 3 left"]

---

**[ITEM NAME]** — [brand] — £[NOW] ~~£[WAS]~~
[Why it's worth looking at]
[Link]

---

*[If only 1-2 deals:] Nothing else worth surfacing today.*

### 5. Update history.md

Log each deal surfaced with date and category.
Track pattern: which categories produce deals, which don't.
Note if user acknowledges / buys (via `/scout bought` command).

---

## Learning over time

history.md builds a pattern of what the user actually acts on.

After 4 weeks:
- Surface more from categories where they've clicked/bought
- Reduce frequency for categories with no engagement
- Weight "currently in market for" items higher

The skill gets sharper the longer it runs.

---

## Management commands

- `/scout now` — run immediately
- `/scout add [item or category]` — add to preferences
- `/scout remove [category]` — stop scanning a category
- `/scout bought [item]` — log a purchase (trains preferences)
- `/scout pause [days]` — pause for X days (holiday mode)
- `/scout history` — show last 30 days of surfaced deals
- `/scout preferences` — show and edit current preferences

---

## What makes it good

The quality bar is everything. Most deal finders are noise.
This one should feel like a friend who spotted something you'd actually want.

Silent on bad deal days. One great deal beats five mediocre ones.

The deal has to be genuinely good, not just discounted.
A £300 item at £270 is not a deal. A £300 item at £180 is.
Always verify the "was" price before surfacing.
