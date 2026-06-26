# Reddit Account Operations

> Operating doctrine for Reddit automation — careful, helpful, non-spam contributor pattern with role separation, post qualification, quotas, anti-spam triggers and recovery.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-orange)](https://clawhub.ai/alexbloch-ia/reddit-account-operations)
[![Version](https://img.shields.io/badge/version-1.2.0-green)](#changelog)

A Claude Code / OpenClaw skill for running Reddit brand accounts safely. Battle-tested in a regulated-field operation, ported to be domain-agnostic.

**Why most Reddit automation gets banned**: it treats Reddit like Twitter. This doctrine doesn't.

---

## What's in the box

- **3-role mental model** for any Reddit account (`red-post` / `red-engage` / `red-stealth`)
- **Karma-phased posting**: Phase A safety net (karma < 100, zero brand mentions) → Phase B (full doctrine, brand-aware) — with **manual override path** for established brands
- **Zero-outgoing-link policy** in replies and posts — the only doctrine that actually survives Reddit automod long-term
- **Human-like posting flow** (new in v1.2.0): how to bypass Reddit's reCAPTCHA Enterprise Invisible on `/api/submit` via UI dwells + slow typing, including the `LC_NUMERIC` macOS trap that silently breaks scripts
- **Strict reply qualification**: age, score, mods, expert-duplicate check, sub freeze
- **Hard quotas** calibrated under spam-filter thresholds (replies/day, posts/week, time-between-actions)
- **Anti-spam triggers**, both content (banned phrases, shorteners-banned) and behavioral (no reply within 60s of post, no >3 actions in 30 min)
- **Sub state tracking**: auto-freeze a sub after two removals
- **Full recovery playbook**: `status:stopped`, HTTP 429, 403, captcha, shadowban suspicion, automod removals
- **Memory file inventory** for stateful agents
- **Mandatory recap pattern** (alert channel + memory)

---

## Install

### Via ClawHub (recommended)

The skill is published on ClawHub — install in one click from your agent:

👉 **<https://clawhub.ai/alexbloch-ia/reddit-account-operations>**

### Via this repository (manual)

Clone and run the install script — it copies `SKILL.md` into your local skills directory.

```bash
git clone https://github.com/AlexBloch-IA/reddit-account-operations.git
cd reddit-account-operations
./install.sh
```

The script detects which agent stack you have and copies the skill there:

- `~/.claude/skills/reddit-account-operations/` (Claude Code)
- `~/.openclaw/skills/reddit-account-operations/` (OpenClaw)
- Both if both are present.

### Manual copy

```bash
mkdir -p ~/.claude/skills/reddit-account-operations
cp SKILL.md ~/.claude/skills/reddit-account-operations/
```

---

## Quick start

1. Open `SKILL.md` and fill the placeholders in **Section 0** (brand, domain, username, browser profile, port, niche keywords, target subs, workspace dir).
2. Wire your crons to follow the doctrine (login check first, qualify before reply, log to memory, recap to your alert channel).
3. **Start in Phase A** until karma ≥ 100. Don't shortcut.

Shell snippets in the skill use the [OpenClaw](https://openclaw.ai) browser CLI as an example automation stack. Swap them for Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool you prefer — the doctrine is stack-agnostic.

---

## Who is this for

Any niche where the brand needs to be a *background* signal behind genuinely useful posts:

- **Legal services** (origin of the doctrine — works under strict bar association rules)
- **Medical / health** practitioners with public-content strategies
- **Financial advisors** subject to compliance constraints
- **SaaS / B2B founders** doing community-led growth
- **Creators / agencies** managing brand accounts on behalf of clients

Anywhere spam = reputation death.

---

## Repository structure

```
reddit-account-operations/
├── SKILL.md         # the skill (full doctrine)
├── README.md        # this file
├── LICENSE          # MIT-0
├── install.sh       # auto-install into ~/.claude/skills or ~/.openclaw/skills
└── CHANGELOG.md     # version history
```

---

## Companion skill

For X / Twitter, see **[twitter-account-operations](https://github.com/AlexBloch-IA/twitter-account-operations)** — same doctrine, ported to X with cron-by-cron playbook.

---

## License

Released under **MIT-0** (MIT No Attribution). Use, fork, adapt, redistribute. No attribution required.

---

## Author

[Alexandre Bloch](https://github.com/AlexBloch-IA) — founder of [OpenClaw](https://openclaw.ai).
Published on [ClawHub](https://clawhub.ai/alexbloch-ia).
