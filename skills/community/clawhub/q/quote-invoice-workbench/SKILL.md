---
name: quote-invoice-workbench
description: Turn messy service pricing notes into professional quotes, SOW line items,
  and invoice drafts with assumptions clearly surfaced.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Quote & Invoice Workbench

## Purpose

Turn messy service pricing notes into professional quotes, SOW line items, and invoice drafts with assumptions clearly surfaced.

## Trigger phrases

- 报价单
- invoice draft
- 做服务报价
- 估算项目费用
- scope and quote

## Ask for these inputs

- service scope
- rate card or budget
- timeline
- payment terms
- optional taxes/discounts

## Workflow

1. Break the scope into clear line items and assumptions.
2. Use the bundled pricebook as a starting point or adapt to the user's rates.
3. Calculate subtotal, taxes, discounts, deposit, and milestones.
4. Generate quote and invoice drafts separately.
5. Make all assumptions explicit to reduce disputes.

## Output contract

- quote table
- invoice draft
- assumptions list
- scope exclusions

## Files in this skill

- Script: `{baseDir}/scripts/quote_calculator.py`
- Resource: `{baseDir}/resources/pricebook.csv`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 报价单
- invoice draft
- 做服务报价

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/quote_calculator.py`.
- Bundled resource is local and referenced by the instructions: `resources/pricebook.csv`.
