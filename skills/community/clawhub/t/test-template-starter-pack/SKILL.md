---
name: test-template-starter-pack
description: Build production-ready Telegram vertical AI agents in 10-15 minutes. Battle-tested template with intent classification, lead scoring, CRM, routing, follow-up, and analytics — the engine behind two deployed agents (27/27 tests).
version: 1.1.0
metadata:
  openclaw:
    emoji: "\U0001F9EA"
    requires:
      bins:
        - python3
    primaryEnv: ""
    envVars: []
    tags:
      - vertical-agent
      - template
      - starter-pack
      - python
      - test-suite
      - crm
      - lead-scoring
      - freemium
when_to_use: "Use when building a new Telegram vertical AI agent — tax bot, real estate CRM, dental reception, legal intake, e-commerce support. Start here, customize the 7-step fill-in process for your vertical, and deploy in minutes."
---

# Test-Deployment Template — Starter Pack

Build production-ready vertical AI agents for Telegram in 10-15 minutes.

## What You Get

A battle-tested Python template (647 lines, 27/27 tests) implementing the full vertical agent pipeline:

```
classify → score → route → CRM → follow-up → analytics → tier-gate → error-handle
```

**Two real-world examples included:** SelfBot (RU tax assistant) and Real Estate Agent (US property CRM).

## Quick Start

```bash
clawhub install test-template-starter-pack
cd skills/test-template-starter-pack
python3 _test-template.py  # 27/27 tests pass
```

Then follow `GUIDE.md` — 7 steps to customize for your vertical.

## Features

- Intent classification with configurable patterns
- Lead scoring (weighted multi-factor)
- Multi-tier routing (free → pro → business → enterprise)
- CRUD CRM with SQLite persistence
- Follow-up pipeline with configurable sequences
- Analytics dashboard (conversion funnel, churn, MRR)
- Tier gating (freemium with limits)
- DB migration + cleanup utilities

## Verticals You Can Build

| Vertical | Build Time | Use Case |
|----------|-----------|----------|
| Tax automation | 15 min | Self-employed tax filing bot |
| Real estate CRM | 15 min | Lead scoring + property matching |
| Dental reception | 10 min | Appointment booking + reminders |
| Legal intake | 10 min | Client screening + case routing |
| E-commerce support | 15 min | Order tracking + returns |

## Requirements

- Python 3.8+
- SQLite3 (built-in)
- No external API dependencies (mock data stores — swap for real APIs)

## Files

```
test-template-starter-pack/
├── SKILL.md          ← this file
├── _test-template.py ← reusable engine (27/27 tests)
├── GUIDE.md          ← 7-step vertical-builder walkthrough
└── examples/
    ├── selfbot-brief.md      ← RU tax assistant example
    └── realestate-brief.md  ← US real estate example
```

## Upgrade Path

Full vertical personas (SelfBot, Real Estate Agent) available on [Claw Mart](https://shopclawmart.com).