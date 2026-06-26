---
name: scannable-reports
description: Format agent outputs for mobile chat apps. Unicode progress bars, sparklines, and status indicators that render perfectly in Telegram, Discord, Slack, WhatsApp — no images needed. Use when creating status updates, dashboards, metrics reports, or any structured information for chat-based delivery. Triggers on status reports, dashboards, metrics, progress updates, or when output needs to be mobile-scannable.
---

# Scannable Reports

Mobile-first formatting for chat apps. Make agent outputs professional and easy to scan.

## Why This Exists

Chat apps render plain text. No charts, no images inline. This skill uses Unicode characters to create visual data that works everywhere.

## Core Patterns

### 1. Progress Bars

```
CPU ███████░░░ 70%
MEM ████░░░░░░ 40%
Tasks ████████░░ 80%
```

**Blocks:** `░` (empty) `▒` (light) `▓` (medium) `█` (full)

**10-char bar formula:** `█` × (value/10), `░` × (10 - filled)

### 2. Sparklines (Trends)

```
24h: ▁▂▃▅▇█▇▅▃▂
Revenue: ▂▃▃▅▆▇█ (up)
Errors: █▅▃▂▁▁▁ (down)
```

**Chars (low→high):** `▁ ▂ ▃ ▄ ▅ ▆ ▇ █`

### 3. Status Indicators

| Emoji | Meaning |
|-------|---------|
| 🟢 | Good / Done / Healthy |
| 🟡 | Warning / In Progress |
| 🔴 | Critical / Blocked / Error |
| 🔥 | Hot / Urgent / Trending |
| ⚡ | Fast / Quick win |

### 4. Monospace Tables

Use triple backticks for alignment:

```
Project     Status    Owner
─────────────────────────────
VIRAL       🟡 WIP    PM
Hackathon   🟢 Ready  PM
Matrix      🔴 Block  Sales
```

### 5. Lead with Signal

Most important first. Assume mobile scanning.

**Bad:**
> I've reviewed the project status and found several items that need attention including...

**Good:**
> 🔴 Matrix blocked
> 🟢 Hackathon ready  
> 🟡 VIRAL 75%

## Example Report

```
📊 Daily Status — Feb 27

🔴 Blocked
• Matrix client (awaiting scope)

🟡 In Progress
• Hackathon ████████░░ 80%
• VIRAL     ██████░░░░ 60%

🟢 Shipped
• Demo script ✓
• Offer doc ✓

📈 Momentum: ▃▅▆▇█
```

## Platform Compatibility

| Platform | Progress | Sparklines | Emoji | Monospace |
|----------|----------|------------|-------|-----------|
| Telegram | ✅ | ✅ | ✅ | ✅ |
| Discord | ✅ | ✅ | ✅ | ✅ |
| Slack | ✅ | ✅ | ✅ | ✅ |
| WhatsApp | ✅ | ✅ | ✅ | ⚠️ Limited |
| iMessage | ✅ | ✅ | ✅ | ❌ |

## Quick Reference

```
Progress:  ░▒▓█
Sparkline: ▁▂▃▄▅▆▇█  
Divider:   ─────────
Status:    🟢🟡🔴🔥⚡
```
