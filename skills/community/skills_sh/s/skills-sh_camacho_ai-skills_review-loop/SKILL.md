---
name: review-loop
description: Use when iterative review-fix cycles are needed on a plan or implementation — bounded loop with severity gating, automatic fixes, and finding disposition.
---

# Review Loop

Bounded review-fix-re-review loop. You are the router — parse intent, select reviewers, run the loop.

## 1. Parse Intent

From natural language after `/review-loop`, determine:
- **Target**: plan or work? Check conversation context, recent activity, user's words.
- **Reviewers**: user-specified, or your judgment. Available: `code-reviewer`, `architect-reviewer`, `security-auditor`, `technical-editor`, `accessibility-tester`, `design-reviewer`, `codex-specialist`. Match to artifact type.
- **Round cap**: default 3. User can say "thorough" (5) or "quick" (1).
- **Severity gate**: default P2 (fix P0-P2, record P3+). User can say "strict" (P1) or "lenient" (P3).

If ambiguous, ask: "Reviewing the plan or the work?"

## 2. Dispatch

- **Plan**: invoke `/plan-review` via Skill tool. Pass round cap. Its internal P0 loop counts as R1.
- **Work**: dispatch reviewer(s) via Agent tool. Request severity-tagged findings (P0-P3).

Untagged findings: treat as P1.

## 3. Loop: Fix, Record, Re-review

For each round (R1..R{cap}):

**a. Triage** findings by severity gate (P0 is highest severity, P3 is lowest):
- **Fix** (higher severity than gate — lower P-number, i.e. P0 through P{gate}): fix immediately. Commit: `fix: address R{N} review findings` with `Co-Authored-By` trailer per AGENTS.md.
- **Record** (lower severity than gate — higher P-number, i.e. P{gate+1}+): record, do not fix.

**b. Record** below-gate findings:
- Plans: append `### Deferred Findings (R{N})` section to the plan file.
- Work: `gh issue create --label review-finding --title "R{N}: <summary>"`. Cap 10/round, 20 total across all rounds. If `gh` unavailable, append to `.branch-context.md`.

**c. Reviewer retention** — zero trust in fixes. A reviewer stays on the panel until they individually return no above-gate findings. Only then are they done.
- R1: full panel
- R2+: only reviewers who had above-gate findings in the prior round re-review
- Reviewers with no above-gate findings are done — they already approved implicitly

**d. Exit when:** all reviewers have individually confirmed clean (converged), OR cap reached, OR DROP verdict.

**e. Recurring findings:** if same finding appears across 2+ rounds, escalate severity by 1 level. If an escalated finding reaches P0 and remains unfixed at cap, stop and hand off to human.

## 4. Summary

```
Review Loop Summary
───────────────────────────────────────
Target:    <plan name or file description>
Rounds:    <N of cap>
Gate:      P<N>

│ Round │ P0 │ P1 │ P2 │ P3+ │ Fixed │ Recorded │
│───────│────│────│────│─────│───────│──────────│

Verdict: APPROVE | ESCALATE
```

APPROVE = all above-gate findings resolved. ESCALATE = unresolved above-gate findings remain — hand off to human.

## Guardrails

- Never modify protected files (see AGENTS.md).
- Hard max: 5 rounds even if user requests more. Note: "thorough" (5) is already the maximum.
- Do not auto-merge or auto-approve. The loop produces a verdict, not an action.
- Plain text output only — cross-surface safe.

## Failure Modes

- `/plan-review` unavailable → dispatch `technical-editor` + `architect-reviewer` directly.
- `gh` not authenticated → degrade to `.branch-context.md` or printed list.
- Reviewer returns DROP → exit immediately, print summary.
- No reviewers available → use `code-reviewer` as minimum viable panel.
