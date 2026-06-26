# RAID Log Update and Status Report Builder

**Platforms:** Claude · Openclaw · Codex
**Domain:** Project Management

## Purpose

Updates a project's RAID log (Risks, Assumptions, Issues, Decisions / Dependencies) from new inputs collected during a reporting period — status-meeting notes, blocker reports, risk emails, decision memos, dependency updates — and produces a stakeholder status report with per-workstream RAG (Red / Amber / Green) ratings, top-3 risks, key issues, key decisions, dependencies needing attention, sponsor asks, and an unresolved-information list. Every RAID entry is labelled NEW / UPDATED / CLOSED / REOPENED so reviewers can scan the delta, and the report is labelled DRAFT for PM and sponsor review.

## When to Use

- Preparing a weekly, fortnightly, or monthly status report for a sponsor or steering committee
- Catching up a project's RAID log after several days of activity (meetings, decisions, blockers, vendor updates)
- Onboarding a project that has been running without disciplined RAID hygiene
- Standing up a fresh RAID log at project initiation
- Aligning multiple workstream leads behind a single delta view before steerco
- Triaging a backlog of unstructured email / chat / memo content into the correct RAID lanes
- Recording a sponsor decision permanently and propagating its effect into linked risks, issues, and dependencies

## What It Does

**Phase 1: Project and Cycle Intake**
1. Captures project name, sponsor, PM, workstreams, reporting cadence, current phase, target go-live, and the prior overall RAG
2. Loads (or initialises) the prior RAID log, assigns IDs by lane (`R-NNN`, `A-NNN`, `I-NNN`, `D-NNN`, `Dep-NNN`) if missing, and parses any free-text PM journal into candidate entries for confirmation

**Phase 2: Input Triage**
3. Collects new inputs across the reporting period — status-meeting notes, blocker reports, decision memos, risk escalations, dependency updates, external events, burn / velocity data
4. Routes each input into the correct RAID lane using a verbal-cue routing table, splitting multi-lane content into separate entries and pausing to confirm any cross-lane re-classification

**Phase 3: Lane-Specific Capture**
5. **Risks**: ID, title, description, workstream, category, probability × impact (1–5 × 1–5), exposure (Low / Medium / High / Very High), proximity, owner, mitigation, contingency, trigger, status, last review date — re-scoring with before/after when updated
6. **Assumptions**: statement, source, validation owner, validation date, validation evidence, linked risk/issue if invalidated, status — and automatic linked-issue creation on invalidation
7. **Issues**: severity (1–4), owner, resolution plan, target resolution date, escalation level with named escalation owner for Sev-3+ — closure requires explicit user confirmation and resolution evidence
8. **Decisions**: append-only ledger with decision-maker, forum, rationale, alternatives, reversibility, and linked-IDs — prior decisions are superseded, never edited
9. **Dependencies**: direction (inbound / outbound), counterparty, need-by date, on-track / at-risk / late / delivered status, owner on both sides, with explicit checks for outbound commitments often missed

**Phase 4: Delta and Status Report**
10. Produces a delta summary block (counts per lane of NEW / UPDATED / CLOSED / REOPENED / SUPERSEDED / VALIDATED / INVALIDATED)
11. Proposes RAG ratings per workstream and overall, with rationale anchored to specific RAID entry IDs, showing direction (↑ / ↓ / →) from prior cycle — and refuses to override the user's RAG call, surfacing disagreement to the sponsor
12. Composes a stakeholder status report in a fixed nine-section structure (Headlines, Progress, Top Risks, Key Issues, Key Decisions, Dependencies, Asks, Milestones, Open Questions) ending with a verbatim review banner

## Output

Two artefacts: a fully updated RAID log with delta summary and per-entry NEW / UPDATED / CLOSED / REOPENED labelling, and a DRAFT stakeholder status report with proposed RAG ratings, top-3 risks, key Sev-3+ issues, key decisions, dependencies needing attention, sponsor asks, upcoming milestones, and an open-questions list — ending with a mandatory review banner that names the sponsor as accountable for the published RAG.

## Notes

This skill **drafts** updates to support — never replace — the PM's judgement and the project sponsor's accountability for the published RAG status. The skill does not opine on individual personnel performance, does not opine on contract enforceability, does not escalate items to legal or HR, and does not publish the status report directly to stakeholders. The skill refuses to manipulate RAG ratings to obscure project condition: if the user pushes for a colour that the underlying RAID entries do not support, the skill records the entries and the disagreement, leaving the call with the sponsor. The skill does not auto-close risks or issues — closure requires explicit user confirmation and resolution evidence. The skill applies the PMI / PRINCE2 RAID convention by default and supports the "A = Actions" variant when the user names the override.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
