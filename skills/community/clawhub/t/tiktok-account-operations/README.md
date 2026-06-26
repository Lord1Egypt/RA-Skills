# TikTok Account Operations

> Operating doctrine for TikTok automation — careful, value-adding creator pattern with role separation, business-suite based DM/comment ops, human-like UI flow, strict anti-shadowban quotas, and recovery patterns.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](#changelog)

A Claude Code / OpenClaw skill for running TikTok brand accounts safely. Battle-tested in a regulated-field operation, ported to be domain-agnostic.

**Why most TikTok automation gets throttled (or banned)**: it treats `/business-suite/comments` like a normal DOM, types via synthetic events, and ignores the iframe + textbox-trap. This doctrine doesn't.

---

## What's in the box

- **3-role mental model** for any TikTok account (`tk-post` / `tk-engage` / `tk-stealth`)
- **Algorithm-trust-phased posting**: Phase A safety net (account < 30 days OR recent CG notice, zero outbound brand-aware) → Phase B (full doctrine) — with **manual override path** for established brands
- **Zero-outgoing-link policy** in comments and DMs (TikTok dampens reach hard on external URLs in user-visible text)
- **Human-like UI flow** — the only thing that actually works inside `/business-suite/`:
  - Physical `cliclick` mouse clicks (the synthetic-event composer is non-functional)
  - The two-textbox trap on the comments page (smallest-`vpY` rule for nested replies)
  - The `cliclick t:` accent encoding trap (silently drops accents in some locales — same family as Reddit's `LC_NUMERIC` trap)
  - Computing screen coordinates from viewport
  - Recommended exit-code convention
- **Strict reply qualification**: language, context-read requirement, troll filter, 7-day per-user cap
- **Hard quotas** calibrated under TikTok soft-block thresholds (replies/day, follow/day, cron-interleave 3-min offset)
- **Anti-spam triggers**, both content (banned phrases, shorteners-banned) and behavioral (no reply within 30s, no >6 actions in 10 min, no burst posting)
- **Sound + hashtag state tracking**: auto-detect shadowbanned hashtags, license-compliance for Business accounts
- **Full recovery playbook**: `status:stopped`, HTTP 429, captcha challenge, "Tap to retry" soft-block, comment-removal automod, account warning banner
- **Memory file inventory** for stateful agents
- **Mandatory recap pattern** (alert channel + memory)

---

## Install

### Via ClawHub

The skill is designed to be published on ClawHub — install in one click from your agent once published.

### Manual copy

```bash
mkdir -p ~/.claude/skills/tiktok-account-operations
cp SKILL.md ~/.claude/skills/tiktok-account-operations/
```

Or for OpenClaw:

```bash
mkdir -p ~/.openclaw/skills/tiktok-account-operations
cp SKILL.md ~/.openclaw/skills/tiktok-account-operations/
```

---

## Quick start

1. Open `SKILL.md` and fill the placeholders in **Section 0** (brand, domain, handle, browser profile, port, niche keywords, primary CTA, workspace dir).
2. Confirm your TikTok account is **Business** or **Creator** — the `/business-suite/` UI requires it.
3. Install `cliclick` (`brew install cliclick`) and grant macOS Accessibility permission to your cron's terminal.
4. Wire your crons: DM check at `:00, :15, :30, :45`, Comment check at `:03, :18, :33, :48` — **never fuse them**.
5. **Start in Phase A** until account_age ≥ 30 days AND followers ≥ 500. Don't shortcut.

Shell snippets in the skill use the [OpenClaw](https://openclaw.ai) browser CLI as an example automation stack. Swap them for Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool you prefer — the doctrine is stack-agnostic. The `cliclick` step is macOS-specific; on Linux use `xdotool`; on Windows use `SendInput` / AutoHotkey.

---

## Who is this for

Any niche where the brand needs to be a *background* signal behind genuinely useful comments and DMs:

- **Legal services** (origin of the doctrine — works under strict bar association rules)
- **Medical / health** practitioners with public-content strategies
- **Financial advisors** subject to compliance constraints
- **SaaS / B2B founders** doing community-led growth
- **Creators / agencies** managing brand accounts on behalf of clients

Anywhere shadowban = reach death.

---

## Repository structure

```
tiktok-account-operations/
├── SKILL.md         # the skill (full doctrine)
├── README.md        # this file
├── LICENSE          # MIT-0
└── CHANGELOG.md     # version history (TBD)
```

---

## Companion skills

- **[reddit-account-operations](https://github.com/AlexBloch-IA/reddit-account-operations)** — same doctrine family, ported to Reddit with karma-phased posting and sub-state tracking.
- **[twitter-account-operations](https://github.com/AlexBloch-IA/twitter-account-operations)** — same doctrine, ported to X/Twitter.
- **instagram-account-operations** — for Meta Business Suite-based IG ops.
- **facebook-account-operations** — for FB Page automation.
- **whatsapp-account-operations** — for BSP-API-driven WhatsApp Business ops (the downstream conversion channel for TikTok leads).

---

## License

Released under **MIT-0** (MIT No Attribution). Use, fork, adapt, redistribute. No attribution required.
