# Retrospective Example

A full retrospective from a real session. For everyday retrospectives the rules in SKILL.en.md are enough; read this when unsure whether to log something or how to merge entries.

## Scenario

A skill-quality session: the engineer had the agent do a quality review, competitor comparison, and absorbed improvements on a new skill. The skill is invoked at session end.

## Extracted Entries

After reviewing the conversation, three workflow issues and one positive signal were identified:

**Entry 1 — overstated claim corrected:**

```json
{"timestamp": "2026-11-13T15:30:00+08:00", "platform": "trae", "area": "review", "result": "corrected", "issue_type": "other", "priority": "medium", "notes": "Agent claimed 'self-test done' but only the structural check had run, no content-level tests; correct behavior: distinguish 'structural check' from 'self-test', never claim what was not done"}
```

Key points: under questioning, the "self-test" turned out to be only the `check.sh` structural validation — a **wrong answer that needed correction** (Iron Law 1: points at a real turn). Notes = one sentence problem + one sentence correct behavior, under 200 characters.

**Entry 2 — same-root issues merged + recurrence mark:**

Two doc gaps surfaced during the session: step 3's skip condition was missing the environment/config case, and a cross-skill relative link broke on standalone install. Both trace to the same rule gap — **skill docs were never reviewed from the standalone-install perspective**. Merged into one entry:

```json
{"timestamp": "2026-11-13T15:31:00+08:00", "platform": "trae", "area": "docs", "result": "failed", "issue_type": "other", "priority": "medium", "notes": "Two doc gaps, same root: docs written without the standalone-install perspective (incomplete skip branches, broken relative links) recurring (occurrence 2); suggest adding to skill completion checklists"}
```

Key points: two turns merged into one entry (Anti-Pattern 5); if the historical log already holds a `area=docs` entry of the same kind, also add `recurring (occurrence N)` and raise priority to at least medium — that is the point of recurrence tracking: once is chance, twice or more is a rule gap.

**Entry 3 — positive signal:**

```json
{"timestamp": "2026-11-13T15:32:00+08:00", "platform": "trae", "area": "review", "result": "success", "issue_type": "none", "priority": "low", "notes": "Real read-only Jira smoke test ran the full flow; the doc gap it exposed was fixed in the same round — the loop works"}
```

## What was NOT logged (examples)

- The engineer interjected "don't push yet" mid-session — a normal clarification, no fix target, not logged.
- The engineer said "good idea" — a compliment, not logged.
- The Jira search returned irrelevant tickets — expected tool behavior (no match ≠ error), not logged.

## Summary Table

| Area | Issue Type | Priority | Notes |
|------|-----------|----------|-------|
| review | other | medium | Overstated claim (self-test) |
| docs | other | medium | Standalone-install perspective gap, recurring (occurrence 2) |
| review | none | low | Smoke-test loop worked (success) |

## File Update Suggestions

- Each skill's completion checklist template → consider a "standalone-install perspective" item
- The skill-authoring workflow's validation phase → distinguish three layers: structural check / content self-test / functional smoke test
