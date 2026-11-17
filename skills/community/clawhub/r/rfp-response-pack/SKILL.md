---
name: rfp-response-pack
description: Bid/RFP response pack — extract requirements from hundreds of tender pages, reverse-engineer the scoring method, generate point-by-point response drafts, deviation tables, and a 28-item disqualification (bid-failure) self-check. The scoring committee grades against the rubric; your bid grows the same way.
version: 1.0.0
author: RAY
license: CC-BY-4.0
tags: [rfp, tender, bid-response, government-sales, enterprise-sales, proposal]
pricing:
  free: Free — 1 bid outline/month
  pro: $49/month — scoring reverse-engineering + template library
  annual: $490/year
  pay_per_use: $29 one-time (single bid)
  enterprise: $299/month (company case library + review link)
tiers:
  - id: free
    name: Free
    price: Free
    quota: Free — 1 bid outline/month
  - id: pro
    name: Pro Monthly
    price: $49/month — scoring reverse-engineering + template library
    quota: unlimited
  - id: annual
    name: Pro Annual
    price: $490/year
    quota: unlimited
  - id: enterprise
    name: Enterprise
    price: $299/month (company case library + review link)
    quota: team unlimited
monetization:
  model: freemium_subscription
  currency: USD
  paywall_trigger: free quota exhausted
  trial_days: 7
  free_trial: true
  upgrade_path: Pro Monthly -> Pro Annual -> Enterprise

---
# RFP Response Pack

## What problem it solves

Bid teams burn 60% of their time on two chores: digging requirements out of a few hundred tender pages, and copy-pasting from past proposals. This pack automates both: **decompose the scoring method first, then write the response against each scored item** — the evaluation committee grades with a rubric, so your bid should be grown from that same rubric.

## Workflow

### Step 1: Tender requirement extraction
Input the tender document (PDF/Word), get a structured summary table:
- Project overview / budget / timeline / delivery location
- **Qualification gates** (hard disqualifiers, flagged separately)
- Scoring rubric itemized with points (technical / commercial / price)
- Key dates (Q&A, submission deadline, opening)

### Step 2: Scoring reverse-engineering
Translate every scored item into a response action:
| Scored item | Points | Response action |
|---|---|---|
| Similar track record | 10 | Pick the 3 best-matching projects within the scoring window, attach contract key pages |
| Technical solution | 30 | Respond item-by-item to the requirements doc: "original text → our approach → deviation table" |
| After-sales SLA | 5 | Commit **above** the tender requirement, never equal |
| … | | |

### Step 3: Response draft generation
- Point-by-point response table (no lazy "see annex" — that's the #1 disqualification trigger)
- Deviation table (compliant-plus / compliant; negative deviations flagged red for decision)
- Technical solution chapter skeleton + per-section bullet prompts

### Step 4: Disqualification self-check (28 items)
Cert validity / signatures & seals complete / bid price words match figures / collusion traps (same MAC, identical typos) / copies & sealing requirements / bid bond receipt…

## Boundaries

Output is **assisted drafting**; final bid must be reviewed by the bid owner and legal before submission. No collusion/bid-rigging assistance of any kind.
