---
name: Worth It — Agent Profitability Tracker
description: Finally know if your AI is paying off. Per-project ROI tracking for OpenClaw agents.
license: proprietary
author: DesertSkyLabs
homepage: https://www.shopclawmart.com/listings/worth-it-agent-profitability-tracker-961a92fb
---
> 💰 **Full version available on ClawMart** — dashboard, Opik integration, historical imports, CSV export.
> **Buy here → https://www.shopclawmart.com/listings/worth-it-agent-profitability-tracker-961a92fb** ($29, one-time)


# Worth It — Agent Profitability Tracker

*By DesertSkyLabs*

Finally know if your AI is paying off. Per-project profitability tracking for OpenClaw agents.

---

You're spending real money on AI. Subscriptions, API tokens, time. The question everyone eventually asks is: **is this actually paying off?**

Worth It answers that question. Per project. With real numbers.

---

## What It Does

Tracks what your AI agent costs against what it actually produces — money saved, money earned, hours you didn't have to spend. Then it tells you whether you're getting your money's worth.

Connects to Opik (cloud or local) to pull token costs automatically. You log value in plain language. It does the math.

---

## Value Logging Commands

Drop these anywhere in conversation with your agent:

```
$saved <amount> <description>     # money saved
$earned <amount> <description>    # money earned
$time <hours> <description>       # hours saved × your hourly rate
$cost <amount> <description>      # manual cost entry
```

Your agent will confirm: `Logged: $80 saved → YouTube Workflow`

---

## Agent Instructions (add to your SKILL.md or system prompt)

Recognize these patterns anywhere in a user message and POST to the API:

- `$saved <amount> <description>` → `entry_type=saved`
- `$earned <amount> <description>` → `entry_type=earned`  
- `$time <hours> <description>` → `entry_type=time` (convert hours × hourly_rate)
- `$cost <amount> <description>` → `entry_type=cost`

```
POST http://localhost:3002/api/value
{
  "project_id": "my-project",
  "entry_type": "saved",
  "amount_usd": 80,
  "description": "avoided hiring a writer"
}
```

After logging, confirm briefly: `Logged: $80 saved → my-project`

---

## Full Version — Worth It Dashboard

The full version includes:
- **Live dashboard** — cards per project, ROI banner, daily chart
- **Opik cloud integration** — token costs pulled automatically
- **Historical cost import** — backdate entries to when you actually started spending
- **CSV export** — full value log export
- **Settings page** — hourly rate, APR, project management
- **Auto-detects projects** from `memory/projects.json` if you use another task tracker
- **Systemd service** — runs on boot, always available

**Get the full version: [shopclawmart.com](https://www.shopclawmart.com) → search "Worth It"**

$29 — one-time. No subscription. Yours forever.

---

## Who Built This

Former CEO of a multi-million dollar ecommerce business. Now a homeschool mom of 5 in Arizona. I built this because I was staring at my own AI bills wondering the same thing you are.

— Kate, DesertSkyLabs

