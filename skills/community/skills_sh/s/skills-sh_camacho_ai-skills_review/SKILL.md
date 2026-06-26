---
name: review
description: Unified review skill — auto-detects plan or code, assembles the right panel, runs a bounded review-fix loop with severity gating. Use when a plan or implementation needs review.
---

# /review

Detects whether to review a plan or code, assembles the right panel, runs the review-fix loop.

## 1. Detect Mode

From args or context:

1. Explicit: `/review plan` or `/review code` — use that.
2. Plan file exists in `ai-workspace/plans/` (non-`.done.md`) and no commits beyond main — **plan mode**.
3. `git diff main...HEAD` produces output — **code mode**.
4. Ambiguous — ask: "Reviewing the plan or the code?"

Optional overrides after mode:
- **Round cap**: default 3. "thorough" (5) or "quick" (1).
- **Severity gate**: defaults differ by mode — **plan mode = P2**, **code mode = P3** (local-merge flow assumes nits are cheaper to fix now than to file as issues). "strict" forces P1, "p2" forces P2, "lenient" forces P3.

## 2. Assemble Panel

### Plan mode (Step 4)

**Lead**: `technical-editor` (always).
**Target**: the plan file.

### Code mode (Step 6)

**Lead**: `code-reviewer` (always).
**Target**: changed files (`git diff main...HEAD`).

### Conditional reviewers (both modes)

Scan the target for signals. Add matching reviewers:

| Signal | Plan mode | Code mode |
|---|---|---|
| Architecture, new modules, DI patterns | `architect-reviewer` | `architect-reviewer` |
| AGENTS.md, config.toml, sync.sh, skills | `codex-specialist` | `codex-specialist` |
| Auth, credentials, tokens, secrets | `security-auditor` | `security-auditor` |
| UI, CSS, components, accessibility | `ui-designer` | `design-reviewer` |

No signal match — run with lead only.

Invoke `/assemble-panel` if available for RETAIN, EXPAND, CONVERGE, and ESCALATE_RECURRING governance. Do not duplicate its policy algebra.

Codex/Cursor: read `.agents/skills/assemble-panel/SKILL.md` and apply inline.

## 3. Dispatch

- **Plan mode**: invoke `/plan-review` via Skill tool. Pass panel and round cap. Its internal P0 loop counts as R1.
- **Code mode**: dispatch panel via Agent tool. Request severity-tagged findings (P0-P3).

Untagged findings: treat as P1.

## 4. Loop: Fix, Record, Re-review

For each round (R1..R{cap}):

**a. Triage** by severity gate:
- **Fix** (P0 through P{gate}): fix immediately. Commit: `fix: address R{N} review findings` with `Co-Authored-By` trailer.
- **Record** (P{gate+1}+): record, do not fix.

**b. Record** below-gate findings:
- Plans: append `### Deferred Findings (R{N})` to the plan file.
- Code: `gh issue create --label review-finding --title "R{N}: <summary>"`. Cap 10/round, 20 total. If `gh` unavailable, append to `.branch-context.md`.

**c–f. Panel governance** — invoke `/assemble-panel` for RETAIN, EXPAND, CONVERGE, ESCALATE_RECURRING.

### Terminal P3 Sweep (code mode, gate = P3)

P3 nits multiply: fixing 15 P3s produces a diff that re-enters the panel and surfaces 15 new P3s. To bound this, the **last** fix round in code mode is a *terminal sweep*:

1. Apply P3 fixes from the round.
2. Commit: `fix: address R{N} review findings (P3 sweep)`.
3. Run validation (typecheck + tests). If any fail, treat the failure as a new round at gate=P2 — the sweep is voided and the loop continues normally.
4. **Do NOT re-dispatch the panel** for another round.
5. Print the summary and exit with verdict APPROVE.

A round is the terminal sweep when **all of**: gate is P3, no P0/P1/P2 findings remain unfixed, and the round surfaced only P3 findings. P0–P2 findings always re-enter the loop normally (terminal sweep applies only to nit-only rounds).

## 5. Summary

```
Review Summary
───────────────────────────────────────
Mode:      plan | code
Target:    <file or diff summary>
Rounds:    <N of cap>
Gate:      P<N>

│ Round │ P0 │ P1 │ P2 │ P3+ │ Fixed │ Recorded │
│───────│────│────│────│─────│───────│──────────│

Verdict: APPROVE | ESCALATE
```

- **APPROVE** — all above-gate findings resolved. Next step:
  - Plan mode → Build (Step 5)
  - Code mode → Archive (Step 7)
- **ESCALATE** — unresolved above-gate findings after cap. Present to human.

## Guardrails

- Never modify protected files (see AGENTS.md).
- Hard max: 5 rounds even if requested higher.
- Never auto-merge or auto-approve. Produces a verdict, not an action.
- Plain text output only — cross-surface safe.

## Fallbacks

- `/plan-review` unavailable → dispatch `technical-editor` + `architect-reviewer` directly.
- `/assemble-panel` unavailable → fall back to `[technical-editor, code-reviewer]`, gate=P2, cap=3.
- `gh` not authenticated → degrade to `.branch-context.md`.
- Reviewer returns DROP → exit immediately, print summary.
