# Subscription Audit

Find what you're actually paying for — and what you can cut.

## What it does

Paste your bank or card transaction CSV and get a complete subscription audit:

- **Tiered action table** — every recurring charge sorted into Cancel 🔴, Review 🟡, or Keep 🟢
- **Annual spend estimate** — total cost and projected savings if you act on the cancels
- **Unknown charge flags** — mangled merchant strings identified or flagged for your confirmation
- **Savings summary** — one-paragraph bottom line with your highest-leverage action

## What you provide

**Option A (recommended):** A bank or credit card CSV export covering 60–90 days. Every major US bank exports this from the account activity page in two clicks.

**Option B (fallback):** A manual list — `Netflix $15.99/mo, Spotify $9.99/mo` — for users who prefer not to share transaction data. Coverage will be lower (forgotten subscriptions won't surface).

## Sample output

```
8 subscriptions found | $142.93/month | $1,715.16/year estimated

| Service     | Amount  | Freq    | Est. Annual | Priority   |
|-------------|---------|---------|-------------|------------|
| Netflix     | $15.99  | Monthly | $191.88     | 🟡 Review  |
| Adobe CC    | $54.99  | Monthly | $659.88     | 🟢 Keep    |
| Calm        | $69.99  | Annual  | $69.99      | 🔴 Cancel  |
| ACH*VNDR8K3 | $19.99  | Monthly | $239.88     | ⚠️ Confirm |

Removing Cancel items saves an estimated $69.99/year.
Highest Review opportunity: Netflix — you have Hulu and Max already active.
```

## Privacy

Your financial data is never stored, logged, or transmitted to any third party by this skill. It passes only through the AI provider you configured in OpenClaw (e.g., Anthropic, OpenAI) — solely for this analysis, with no retention between sessions. For fully offline processing, configure Ollama as your model provider in OpenClaw settings.

## Go further — the companion tracker

This skill does the one-time audit. The **Subscription Audit Tracker** is the system that catches new charges going forward and walks you through cancelling cleanly:

- 50+ row tracker — annual cost auto-calculates, status color-codes, 90-day review system
- Live dashboard — Active spend, Pending Review, **Saved-via-cancellation** counter
- Cancellation Playbook for **30 of the most common services** — direct cancel URLs + counter-scripts so retention pages don't keep you
- Excel + Google Sheets compatible

**Launch price $9** (rises to $15 after first 25 buyers / 30 days):
**https://zepoldani.gumroad.com/l/huqic**

## Requirements

No API keys. No external integrations. Works entirely within your OpenClaw session.
