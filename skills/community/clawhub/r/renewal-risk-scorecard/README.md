# Renewal Risk Scorecard

**Platforms:** Claude · Openclaw · Codex
**Domain:** Customer Success

## Purpose

Scores the renewal risk of a single SaaS account across multi-signal health dimensions and produces a save playbook with stakeholder mapping. Designed for the customer success manager preparing a QBR, EBR, renewal-forecast meeting, or escalating a red account to leadership.

## When to Use

- CSM preparing a renewal forecast for an upcoming quarter
- CS leader reviewing at-risk accounts before a renewal review meeting
- CSM building a QBR or EBR for a strategic account
- CS / RevOps triaging a freshly received red-flag signal (NPS detractor, exec change, support spike)
- Account team preparing a save-play workshop for a renewal in jeopardy

## What It Does

**Phase 1: Account Intake**
1. Collects ARR, renewal date, contract type, segment, primary champion, and executive sponsor — one question at a time
2. Captures every relevant signal across five dimensions: product usage, support burden, commercial health, relationship strength, and outcome attainment

**Phase 2: Signal Scoring**
3. Scores each dimension Red / Yellow / Green with a written justification tied to the supplied signals
4. Clusters signals into patterns (e.g., usage drop + champion departure + open critical ticket) — single signals are treated as noise unless severe
5. Produces an overall risk tier (Low / Medium / High / Critical) with rationale

**Phase 3: Save Playbook**
6. Drafts a stakeholder map (champion, economic buyer, detractors, missing relationships)
7. Builds a save playbook: top three actions in priority order with owner, due date, and the dimension they address
8. Drafts a customer-facing talking-points block for the next conversation
9. Writes an internal escalation note for CS leadership with the explicit ask

## Output

A structured renewal scorecard: account header, dimension table with Red/Yellow/Green scores and justifications, signal-cluster summary, overall risk tier, stakeholder map, save playbook table, talking points, and an escalation note. Ready to drop into a CRM, CS platform, or QBR deck.

## Safety Notes

The skill never invents account telemetry, usage numbers, NPS scores, or stakeholder names — every signal must come from the user. If a dimension has no signal at all, it is scored "insufficient data" rather than Green. Account names, ARR figures, and stakeholder identities supplied in the session are treated as confidential and never reused in examples or external lookups.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.