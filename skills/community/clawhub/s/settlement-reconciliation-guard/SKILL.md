---
name: settlement-reconciliation-guard
description: Build a settlement reconciliation brief for marketplace, PSP, and bank payout workflows. Use when a team needs to separate true cash discrepancies from timing effects, fee issues, refund timing, reserve leakage, or order-to-payout mapping gaps.
---

# Settlement Reconciliation Guard

## Overview

Settlement Reconciliation Guard turns a short finance or operations prompt into a structured reconciliation-control brief.
It is useful when you need a fast view of likely discrepancy themes, evidence requirements, matching logic, and close controls for payout reviews.

## Use this skill when

- daily or weekly settlement checks are surfacing unexplained differences
- month-end close needs a tighter review of payout, fee, refund, reserve, or tax treatment
- a team is investigating a missing payout, short payment, or unreconciled batch
- a new marketplace, PSP, or payout channel is being onboarded and needs control design
- finance needs a concise investigation brief before escalating to a provider or posting journals

## What the skill does

The handler reads the prompt, infers likely review context, and produces a structured brief with:

1. **Review mode** such as daily payout check, weekly exception sweep, month-end close support, discrepancy investigation, or new channel setup review
2. **Channels in scope** such as marketplace settlement, PSP/card acquiring, bank remittance, or ERP ledger workflows
3. **Evidence referenced** such as order ledgers, payout reports, bank statements, fee schedules, refund logs, reserve logs, or tax files
4. **Primary discrepancy themes** such as missing payout, fee mismatch, refund timing mismatch, reserve leakage, order-to-payout mapping gaps, or tax variance
5. **Investigation priorities and close controls** that help separate timing differences from true financial loss

## Recommended input patterns

Use plain language. Helpful details include:

- review cadence or close context
- channel or provider involved
- evidence sources available
- known discrepancy symptoms
- whether the issue is a routine review, escalation, or new-channel setup

Example prompts:

- `Need month-end close support for payout and refund timing review.`
- `Investigate missing payout, fee mismatch, and unreconciled batch differences.`
- `Compare Amazon payout report with bank statement and fee schedule before posting to the ERP general ledger.`
- `Create a weekly exception sweep for refund, reserve, and fee variance issues.`

## Output shape

The skill returns a markdown brief with sections such as:

- Reconciliation Summary
- Matching Logic Table
- Discrepancy Queue
- Investigation Priorities
- Close Controls
- Assumptions and Limits

## Boundaries

- This skill is heuristic. It does not query live settlement portals, PSP dashboards, bank feeds, or ERP systems.
- It helps structure reconciliation thinking and evidence review, not replace accounting judgment or provider-side investigation.
- Final journal treatment, dispute escalation, reserve handling, and approval decisions should remain human-approved.
