# Matching rubric (installed pool)

## Scoring dimensions (0–100 total)

Allocate points and **document sub-scores** on every P02b row (`subscores` in JSON). Sub-scores **must sum** to total `score`.

| Dimension | Max points | JSON key | Guidance |
|-----------|------------|----------|----------|
| Outcome fit | 40 | `outcome_fit` | Skill text covers the **same deliverables** as the JD, not just shared keywords |
| Competency coverage | 30 | `competency_coverage` | Each `must_have` mapped in coverage matrix; major gap −8 to −12 equivalent |
| Tool / stack fit | 15 | `tool_stack_fit` | Languages, CLIs, MCP, browsers align with `tools_and_access` |
| Quality / safety posture | 10 | `quality_safety` | Validation, scope discipline, safe patterns in skill text |
| Freshness / trust | 5 | `freshness_trust` | Maintainer signal, narrow scope, no red flags |

## Default thresholds

Stored in `registry.json` → `matching`:

- **`delegate_min_score`**: 75 — auto route with P03.
- **`confirm_band_min`**: 60 — show top 2, recommend one, ask user.
- Below **60** — recruit (P04).

Override per org: lower delegate only if incidents show low false positives.

## Hard negatives and near-neighbor disambiguation

When two+ skills share vocabulary or stack, **do not** split the tie on keyword count alone.

1. **Outcome vs tooling** — Penalize if the skill optimizes for the **wrong primary artifact** (e.g. longform SEO article skill for an **audit** JD).
2. **Review vs implement** — Security **review** skills lose to implementation skills if the JD demands shipping code; the converse if the JD asks for findings only.
3. **Meta vs domain** — `skill-hr` must not win business JDs; domain skills must not win **skill workforce** JDs (see [`matching-lexicon.md`](matching-lexicon.md)).
4. **Candidate-side vs hiring-manager** — Resume **writing** ≠ interview **design** from a resume.
5. **Record `hard_negative_explanations`** in P02 output for runner-ups: one line **why** the higher-scoring neighbor is rejected (scope, missing MCP, wrong vendor API, etc.).

## Registry `notes` and empirical stats

- Read **`skills[].notes`** in `registry.json` when present: treat as HR annotations (e.g. “strong for forms, weak for OCR”)—adjust `competency_coverage` or `outcome_fit` and cite in evidence.
- **Tie-breakers** (in order): higher `tasks_success / max(tasks_total, 1)`; more recent `last_used_at`; higher raw `score`; alphabetic `skill_id`.
- When breaking a tie, add one sentence to **`decision_rationale`** or per-candidate evidence stating **which tie-break step** decided (for auditability).

## Probation adjustments

- If candidate `status: on_probation`, require **+5 score margin** over second place to auto-delegate; else `confirm`.

## Exclusions

- `terminated`, `frozen`: score = N/A, omit from ranking.
- `skill-hr`: exclude from business JD matching (meta-tasks only).

## Example evidence line

> "Description states 'comprehensive PDF manipulation' and lists form filling; JD requires PDF form extraction—strong outcome fit (+36/40)."
