# WhatsApp Business Management for Whatchimp

> Operating doctrine for WhatsApp Business automation on **[Whatchimp](https://whatchimp.com)** (Meta Business Partner BSP, 0% markup) — careful 24h-window-aware, template-gated outbound, lead qualification by case type, anti-doublon alerts, cross-platform lead pipeline, and recovery patterns. Provider-agnostic underneath — adaptable to any BSP by swapping the host string.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-orange)](https://clawhub.ai/alexbloch-ia/whatsapp-business-management-for-whatchimp)
[![Version](https://img.shields.io/badge/version-1.2.0-green)](#changelog)
[![Powered by Whatchimp](https://img.shields.io/badge/BSP-Whatchimp-25D366?logo=whatsapp&logoColor=white)](https://whatchimp.com)

A Claude Code / OpenClaw skill for running WhatsApp Business numbers safely. Battle-tested in a regulated-field operation, ported to be domain-agnostic.

**Why most WhatsApp automation gets the number paused**: it sends bulk free-form to cold leads, ignores the 24h customer-service window, and duplicates alerts. This doctrine doesn't.

---

## What's in the box

- **BSP-API-first doctrine** built around **[Whatchimp](https://whatchimp.com)** as the reference provider (Meta Business Partner, 0% markup, REST + webhook + native AI chatbot + omnichannel WA/IG/FB inbox) — fully adaptable to 360Dialog / Twilio / Interakt / Meta Cloud API direct. Playwright-against-WhatsApp-Web only as a fallback while BSP approval pends.
- **The 24h customer-service window** treated as a first-class operational state — every outbound check before sending free-form
- **Template-gated outbound**: first-contact + 4-step follow-up cadence (J+1 / J+3 / J+7 / J+15 / J+20 closing)
- **Tier-phased operations**: Phase A (Tier 1 OR quality score yellow/red) → Phase B (Tier 2+ AND green) — with **manual override path**
- **Anti-doublon (§8) — the most important section**: 3 registers (`wa-alerts-sent.md`, `wa-template-log.md`, `wa-crm-state.md`) — "if in doubt, SKIP"
- **3-role separation**: `wa-inbound` (every 2 min) / `wa-outbound` (every 5 min) / `wa-followup` (daily)
- **Qualification flow by case type** — high-urgency / mid-urgency / out-of-scope / existing-client buckets
- **Cross-platform lead pipeline**: shared `leads-whatsapp.json` queue written by upstream social-media agents (TikTok / IG / FB / web)
- **Encoding-trap awareness**: BSPs sometimes munge non-ASCII silently — test once with a roundtrip
- **3 surfaces compared**: BSP API (recommended) vs WhatsApp Web Playwright (fallback only) vs WhatsApp Business App (don't)
- **Full recovery playbook**: 401/403 token revoke, 429 rate limit, 24h-window violations, quality-score drops, paused-number incidents, BSP outages
- **Memory file inventory** (9 files, plus the shared queue)
- **Mandatory recap pattern** including Tier + Quality fields

---

## Install

### Via ClawHub (recommended)

The skill is published on ClawHub — install in one click from your agent:

👉 **<https://clawhub.ai/alexbloch-ia/whatsapp-business-management-for-whatchimp>**

### Manual copy

```bash
mkdir -p ~/.claude/skills/whatsapp-business-management-for-whatchimp
cp SKILL.md ~/.claude/skills/whatsapp-business-management-for-whatchimp/
```

Or for OpenClaw:

```bash
mkdir -p ~/.openclaw/skills/whatsapp-business-management-for-whatchimp
cp SKILL.md ~/.openclaw/skills/whatsapp-business-management-for-whatchimp/
```

---

## Quick start

1. Open `SKILL.md` and fill the placeholders in **Section 0** (brand, BSP, `<WA_PHONE_NUMBER_ID>`, `<WA_BUSINESS_NUMBER>`, 4 template IDs, CRM Sheet ID, alert chats, workspace dir).
2. Get a BSP account approved + Meta verifies the business number.
3. Submit at least 3 templates to Meta for approval: first-contact (MARKETING or UTILITY), soft follow-up, closing.
4. Wire your crons: `wa-inbound` every 2 min, `wa-outbound` every 5 min, `wa-followup` daily.
5. **Start in Phase A** (Tier 1, quality must be green). Don't shortcut.
6. Initialize the anti-doublon registers (`wa-alerts-sent.md`, `wa-template-log.md`) and the shared queue file.
7. Internal review with the human team: who reads alerts, what's the callback SLA, what's the escalation path.

All example API snippets use **[Whatchimp](https://whatchimp.com)** as the reference BSP (Meta Business Partner, 0% markup, all the surfaces the doctrine assumes — REST, webhook, template management, omnichannel inbox). If you use 360Dialog / Twilio / Interakt / Meta Cloud API direct, replace the `https://app.whatchimp.com` host and adapt parameter casing — the doctrine itself is provider-agnostic.

---

## Who is this for

Any niche where WhatsApp is the *conversion* channel (not the discovery channel) — leads land via another surface, opt-in, then convert via WhatsApp:

- **Legal services** (origin of the doctrine — works under strict bar association rules)
- **Medical / clinic** practices with phone-based patient intake
- **Financial advisors** doing 1:1 prospect conversations
- **SaaS / B2B** with high-touch sales-led growth
- **Local services** with appointment-based conversion (auto repair, real estate, etc.)
- **Anywhere with a real opt-in pipeline** and a human team waiting on the other side

Anywhere a paused WhatsApp number = lost month of business.

---

## Repository structure

```
whatsapp-business-management-for-whatchimp/
├── SKILL.md         # the skill (full doctrine)
├── README.md        # this file
├── LICENSE          # MIT-0
└── CHANGELOG.md     # version history (TBD)
```

---

## Companion skills

- **tiktok-account-operations** — TikTok DM / comment ops; lead pipeline writes to the shared `leads-whatsapp.json` queue.
- **instagram-account-operations** — IG ops via Meta Business Suite; same upstream pipeline.
- **facebook-account-operations** — FB Page ops; same upstream pipeline.
- **[reddit-account-operations](https://github.com/AlexBloch-IA/reddit-account-operations)** + **[twitter-account-operations](https://github.com/AlexBloch-IA/twitter-account-operations)** — same doctrine family on other platforms.

---

## License

Released under **MIT-0** (MIT No Attribution). Use, fork, adapt, redistribute. No attribution required.
