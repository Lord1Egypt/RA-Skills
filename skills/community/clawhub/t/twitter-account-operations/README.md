# X / Twitter Account Operations

> Operating doctrine for X / Twitter automation — stable Chrome sessions, role separation, careful posting, reply discipline, recovery patterns.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-orange)](https://clawhub.ai/alexbloch-ia/twitter-account-operations)
[![Version](https://img.shields.io/badge/version-1.1.0-green)](#changelog)

A Claude Code / OpenClaw skill for running X brand accounts safely. Battle-tested in a regulated-field operation, ported to be domain-agnostic.

**Why most X automation looks robotic and gets throttled**: it treats the browser like an API. This doctrine doesn't.

---

## What's in the box

- **3-role mental model** for any X account (`tw-post` / `tw-engage` / `tw-stealth`)
- **Human-like browser discipline**: open the right page first, let the UI load, read before clicking, click once and verify
- **Full cron-by-cron playbook**: weekly planning, notifications check, keyword monitor (morning/midday/evening), reply pass, original posts (morning/noon/evening), thread generator, result publish, daily metrics recap
- **Strict reply qualification** — no impulse posting, no generic CTAs, no expert-grade advice in public
- **Full recovery playbook**: browser down, browser frozen, account cockpit unstable, too many tabs, composer stuck, page unusable
- **Explicit anti-patterns** to avoid

---

## Install

### Via ClawHub (recommended)

The skill is published on ClawHub — install in one click from your agent:

👉 **<https://clawhub.ai/alexbloch-ia/twitter-account-operations>**

### Via this repository (manual)

Clone and run the install script — it copies `SKILL.md` into your local skills directory.

```bash
git clone https://github.com/AlexBloch-IA/twitter-account-operations.git
cd twitter-account-operations
./install.sh
```

The script detects which agent stack you have and copies the skill there:

- `~/.claude/skills/twitter-account-operations/` (Claude Code)
- `~/.openclaw/skills/twitter-account-operations/` (OpenClaw)
- Both if both are present.

### Manual copy

```bash
mkdir -p ~/.claude/skills/twitter-account-operations
cp SKILL.md ~/.claude/skills/twitter-account-operations/
```

---

## Quick start

1. Open `SKILL.md` and fill the placeholders in **Section 0** (brand, domain, handle, browser profile, port, niche keywords, workspace dir).
2. Wire your crons to follow the doctrine (right page first, read before acting, verify after each action).
3. **Always have a local draft fallback** — never compose directly in the browser without backup.

Shell snippets in the skill use the [OpenClaw](https://openclaw.ai) browser CLI as an example automation stack. Swap them for Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool you prefer — the doctrine is stack-agnostic.

---

## Who is this for

Any niche where the brand needs to be a *background* signal behind genuinely useful posts:

- **Legal services** (origin of the doctrine — works under strict bar association rules)
- **Medical / health** practitioners with public-content strategies
- **Financial advisors** subject to compliance constraints
- **SaaS / B2B founders** doing community-led growth
- **Creators / agencies** managing brand accounts on behalf of clients

Anywhere account safety > raw reach.

---

## Repository structure

```
twitter-account-operations/
├── SKILL.md         # the skill (full doctrine)
├── README.md        # this file
├── LICENSE          # MIT-0
├── install.sh       # auto-install into ~/.claude/skills or ~/.openclaw/skills
└── CHANGELOG.md     # version history
```

---

## Companion skill

For Reddit, see **[reddit-account-operations](https://github.com/AlexBloch-IA/reddit-account-operations)** — same doctrine, ported to Reddit with karma-phased posting and sub-state tracking.

---

## License

Released under **MIT-0** (MIT No Attribution). Use, fork, adapt, redistribute. No attribution required.

---

## Author

[Alexandre Bloch](https://github.com/AlexBloch-IA) — founder of [OpenClaw](https://openclaw.ai).
Published on [ClawHub](https://clawhub.ai/alexbloch-ia).
