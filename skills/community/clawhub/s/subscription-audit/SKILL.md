---
slug: subscription-audit
name: Subscription Audit
description: Analyze a bank or card CSV export to surface forgotten, unused, or redundant subscriptions. Categorizes into cancel / review / keep tiers, estimates annual spend, and outputs a markdown action table. Trigger when a user pastes transaction history or a manual subscription list and asks what they're paying for, what to cancel, or how much recurring charges are costing them.
version: 1.0.0
license: MIT
tags:
  - finance
  - personal-finance
  - subscriptions
  - budgeting
  - spending
metadata:
  openclaw:
    requires:
      env: []
      bins: []
---

# Subscription Audit

Turn a bank or card transaction export into a clear, prioritized action table — tiered by cancel / review / keep priority, with estimated annual spend and savings. No spreadsheet required.

## When to use this skill

Trigger this skill when the user:
- Pastes a bank or credit card CSV export and asks about subscriptions, recurring charges, or what they're paying for
- Says "audit my subscriptions," "find my recurring charges," "what am I subscribed to," "what can I cancel"
- Pastes a manual list of subscriptions and asks for analysis or prioritization
- Asks how much they're spending on subscriptions per month or per year

Do NOT trigger for:
- Full budget analysis across all income/expense categories — out of scope
- One-time or non-recurring charges
- Investment or savings account analysis

---

## Step 1 — Collect input

Ask the user to provide one of the following. Do not ask for both simultaneously.

### Option A: CSV export (preferred)

Bank or card transaction export covering at least 60–90 days. Most banks export from the account activity page under "Download" or "Export."

**Ask the user to paste CSV contents directly into chat.** Supported formats from all major US banks and credit unions. Minimum useful columns: Date, Description/Merchant, Amount. Accept any superset (Category, Type, etc.) — ignore what you don't need.

### Option B: Manual list (fallback)

If the user doesn't have a CSV or prefers not to share one, accept any format:
- `Netflix $15.99/mo, Spotify $9.99/mo, Adobe CC $54.99/mo`
- A rough list from memory
- A copy-paste from their email receipts

State this limitation once and only once: *"Manual lists may miss forgotten subscriptions that don't appear from memory — a bank CSV gives fuller coverage."*

---

## Step 2 — Identify and classify subscriptions

### Rules-based pass (apply first, no LLM tokens)

Flag as subscription if the merchant name matches known patterns:

**Streaming & media:** Netflix, Hulu, Disney+, Max, Peacock, Paramount+, Apple TV+, Amazon Prime, Spotify, Apple Music, Tidal, Pandora, YouTube Premium, SiriusXM, Audible, Kindle Unlimited

**Software & SaaS:** Adobe, Microsoft 365, Google One, Dropbox, iCloud, Notion, Canva, Grammarly, LastPass, 1Password, NordVPN, ExpressVPN, Mullvad, Zoom, Slack, GitHub, Figma, Loom, Webflow, Squarespace, Wix, Mailchimp, ConvertKit, Beehiiv

**News & content:** NYT, WSJ, Washington Post, The Atlantic, Substack, Patreon, Medium

**Fitness & wellness:** Peloton, ClassPass, Planet Fitness, Equinox, Calm, Headspace, Nike Training Club, Noom, Weight Watchers

**Food & delivery:** HelloFresh, EveryPlate, Factor, Sunbasket, Green Chef, DoorDash DashPass, Instacart+, Gopuff

**Personal finance tools:** Credit Karma, LifeLock, IdentityForce, Rocket Money, YNAB, Copilot

**Telecom:** Cell carriers, internet providers — flag as recurring but mark 🟢 Keep by default; don't recommend cancel without explicit user input

**Amazon:** Distinguish Prime membership from retail purchases by merchant string pattern

### LLM-assisted pass (second pass for unknowns)

For mangled or unrecognized merchant strings (e.g., `AMZN*MX7K3B`, `VZWRLSS*APOP`, `ACH DEBIT 123456`):
- Use amount, frequency, and partial name to infer the service
- If confident (>80%), classify it and note the inference
- If uncertain, flag explicitly as: ⚠️ Confirm — do not guess and present it as fact

### Frequency inference

Use recurrence across the date range to infer billing cycle:
- **Monthly:** charge appears ~every 28–31 days
- **Annual:** single large charge from a known annual biller — label as annual, not monthly
- **Weekly:** flag separately; uncommon for subscriptions, may be a gig or delivery service

---

## Step 3 — Output the audit

Deliver the full audit in a single response. Structure:

### Privacy note (once per session, not repeated on follow-ups)

> 🔒 **Privacy note:** This skill does not store, log, or transmit your financial data to any third party. Your transaction data passes only through the AI provider you configured in OpenClaw (e.g., Anthropic, OpenAI) — solely for this analysis, with no retention between sessions. For fully offline processing, configure Ollama as your model provider in OpenClaw settings.

### Summary line

> **X subscriptions found | $Y/month | $Z/year estimated**

### Audit table

| Service | Amount | Freq | Est. Annual | Category | Priority |
|---|---|---|---|---|---|
| Netflix | $15.99 | Monthly | $191.88 | Streaming | 🟡 Review |
| Adobe CC | $54.99 | Monthly | $659.88 | Software | 🟢 Keep |
| Calm | $69.99 | Annual | $69.99 | Wellness | 🔴 Cancel |
| ACH\*VNDR8K3 | $19.99 | Monthly | $239.88 | ? | ⚠️ Confirm |

**Priority tier definitions:**

- 🔴 **Cancel** — no recent activity pattern, clear duplicate of another active service, or user has explicitly said it's unused. Only assign Cancel when there is evidence — not by assumption.
- 🟡 **Review** — possibly underused, has a direct competitor already in the Keep column, or is a category with 2+ overlapping services. Recommend the user make an active decision.
- 🟢 **Keep** — clearly active and earning its cost, or a utility/telecom where cancellation has major downstream effects.
- ⚠️ **Confirm** — merchant identity uncertain; do not classify until user confirms.

**Assignment rule:** When in doubt between 🔴 and 🟡, use 🟡. Never auto-assign Cancel without a clear reason.

### Savings summary

After the table, one short paragraph:
- Total estimated annual spend across all subscriptions
- Estimated annual savings if all 🔴 Cancel items are removed
- The single highest-leverage 🟡 Review item and why it's worth a decision

---

## Step 4 — Follow-up offers

After delivering the audit, offer once:

- "Want a focused view of just the 🔴 Cancel items with step-by-step cancellation links?"
- "Want to re-run this with a different date range or more transactions?"
- "Want to track these going forward and get an alert if new recurring charges appear?"

Do not auto-regenerate or add analysis unless explicitly asked.
