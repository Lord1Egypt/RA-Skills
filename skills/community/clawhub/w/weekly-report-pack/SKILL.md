---
name: weekly-report-pack
description: Auto-generate structured weekly/daily/monthly reports from scattered work traces — chats, todos, calendar, git commits, notes. Quantified wins, risks with actions taken, deliverable-oriented next steps. Multi-audience versions (manager / cross-team / exec).
version: 1.0.0
author: RAY
license: CC-BY-4.0
tags: [reporting, status-update, productivity, standup, writing]
pricing:
  free: Free — 3 reports/week, single audience, no charts
  pro: $9/month — unlimited + monthly template + multi-audience versions + chart suggestions
  annual: $90/year
  pay_per_use: $5 one-time (single custom report)
  enterprise: $99/month (team template + bulk generation)
tiers:
  - id: free
    name: Free
    price: Free
    quota: Free — 3 reports/week, single audience, no charts
  - id: pro
    name: Pro Monthly
    price: $9/month — unlimited + monthly template + multi-audience versions + chart suggestions
    quota: unlimited
  - id: annual
    name: Pro Annual
    price: $90/year
    quota: unlimited
  - id: enterprise
    name: Enterprise
    price: $99/month (team template + bulk generation)
    quota: team unlimited
monetization:
  model: freemium_subscription
  currency: USD
  paywall_trigger: free quota exhausted
  trial_days: 7
  free_trial: true
  upgrade_path: Pro Monthly -> Pro Annual -> Enterprise

---
# Weekly Report Pack

## What problem it solves

Writing status reports isn't about typing — it's about **organization**: which of the 20 things you did this week actually matter, how to quantify wins without sounding like a brag sheet, and how to surface problems without looking helpless. This pack turns "scattered traces → structured report" into a repeatable pipeline.

## Workflow

1. **Feed**: dump this week's work traces — chat logs, checked todos, calendar, git commits, notes. Any format.
2. **Pick template**: `daily` (3-part) / `weekly` (5-part) / `monthly` (business view). First run: confirm the audience (direct manager / cross-team / exec) — audience controls depth and tone.
3. **Generate**, conclusion-first:
   - **Core progress** (max 3 items, each = result + number + impact)
   - **Key metrics** (WoW delta; if no data, suggest how to collect it)
   - **Issues & risks** (format: issue + mitigation already taken + support needed — never a naked complaint)
   - **Next week** (deliverable-oriented, dependencies flagged)
4. **Format**: Markdown / email body / Slack or Teams message.

## Quality rules

- Every progress item must answer "so what" — what it means for the team/project.
- Numbers first: never write "significantly improved" when a number exists.
- Every issue must carry an action, otherwise it goes to "observations".
- Compare against last week's report to avoid re-reporting the same progress (user pastes last week's version).

## Boundaries

Never fabricate data; unprovided metrics marked as [TBD]. Neutral wording on other people's performance.
