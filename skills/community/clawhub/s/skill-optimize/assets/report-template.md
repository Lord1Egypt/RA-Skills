# Skill Optimization Report

> **Target skill:** `<path-to-skill>`
> **Audit date:** `<YYYY-MM-DD>`
> **Auditor:** `skill-optimizer`

---

## Summary

A 3-dimension audit of the target skill. Top-line finding first; details below.

**Overall verdict:** `<Healthy | Needs polish | Needs refactor | Rewrite recommended>`

**Top 3 changes** (ranked by leverage):

1. `<one-sentence change>` — Dimension `<1|2|3>`, severity `<Blocker|Major|Minor>`
2. `<one-sentence change>` — Dimension `<1|2|3>`, severity `<Blocker|Major|Minor>`
3. `<one-sentence change>` — Dimension `<1|2|3>`, severity `<Blocker|Major|Minor>`

**Findings tally:** `<n>` blockers, `<n>` majors, `<n>` minors, `<n>` nits.

**Effort estimate:** `<trivial edit | focused refactor | substantial rewrite>`

---

## Dimension 1 — Specification compliance

> Mechanical, binary checks from `references/specification-checklist.md`. Run `scripts/audit_skill.py <path>` to populate.

**Verdict:** `<Pass | Warning | Fail>`

| Check | Result | Evidence |
|---|---|---|
| `SKILL.md` exists | ✅ / ❌ | — |
| Frontmatter present and well-formed | ✅ / ❌ | — |
| `name` is kebab-case, 1–64 chars | ✅ / ❌ | — |
| `name` matches parent directory | ✅ / ❌ | — |
| `description` is 1–1024 chars, no angle brackets | ✅ / ❌ | — |
| `compatibility` (if present) is 1–500 chars | ✅ / ❌ | — |
| No unexpected frontmatter keys | ✅ / ❌ | — |
| Body ≤ 500 lines | ✅ / ❌ | — |
| No extra `---` fences in body | ✅ / ❌ | — |
| Referenced files exist and are 1-level deep | ✅ / ❌ | — |

**Blockers / majors in this dimension:**

- `<CODE>: <message> — fix: <fix>`

---

## Dimension 2 — Best practices alignment

> Content-quality checks from `references/best-practices-checklist.md`. LLM judgment, not regex.

**Verdict:** `<Pass | Warning | Fail>`

| Axis | Verdict | One-line evidence |
|---|---|---|
| Scope (one coherent unit) | ✅ / ⚠️ / ❌ | — |
| Specificity calibration (flex vs prescriptive) | ✅ / ⚠️ / ❌ | — |
| Defaults, not menus | ✅ / ⚠️ / ❌ | — |
| Procedure over declaration | ✅ / ⚠️ / ❌ | — |
| Gotchas section | ✅ / ⚠️ / ❌ | — |
| Output templates | ✅ / ⚠️ / ❌ | — |
| Progressive disclosure (≤500 lines, references with triggers) | ✅ / ⚠️ / ❌ | — |
| Token budget (omits what the agent already knows) | ✅ / ⚠️ / ❌ | — |
| Reusable scripts (bundled when work is repeated) | ✅ / ⚠️ / ❌ | — |
| Validation loops (self-check before finalizing) | ✅ / ⚠️ / ❌ | — |

**Issues in this dimension:**

- `<axis>: <issue> — suggested fix: <fix>`

---

## Dimension 3 — Description optimization

> Wording checks from `references/description-guide.md`. The description is the *only* triggering signal.

**Verdict:** `<Pass | Warning | Fail>`

| Check | Result | Evidence |
|---|---|---|
| Imperative framing ("Use this skill when...") | ✅ / ⚠️ / ❌ | — |
| Both WHAT and WHEN present | ✅ / ⚠️ / ❌ | — |
| Pushy catch-all (catches near-misses) | ✅ / ⚠️ / ❌ | — |
| Concrete keywords (file types, domain, verbs) | ✅ / ⚠️ / ❌ | — |
| Length 200–500 chars (well under 1024) | ✅ / ⚠️ / ❌ | — |
| No angle brackets, no vague verbs | ✅ / ⚠️ / ❌ | — |
| Doesn't start with "I" / "This skill" | ✅ / ⚠️ / ❌ | — |

**Proposed rewrite** (apply only after user approval):

```yaml
# Before
description: <current description>

# After
description: <proposed description, with one-sentence note on why each change improves triggering>
```

**Why this rewrite helps:**

- `<change 1 — why>`
- `<change 2 — why>`
- `<change 3 — why>`

---

## Anti-patterns flagged

From `references/common-issues.md`. Each row: pattern observed, evidence, fix.

| # | Pattern | Evidence | Fix |
|---|---|---|---|
| 1 | — | — | — |
| 2 | — | — | — |
| 3 | — | — | — |

---

## Proposed edits (concrete diffs)

> Apply only with user approval. Show each diff and wait.

### Edit 1 — `<description>`

```diff
- <before>
+ <after>
```

**Rationale:** `<one-sentence reason this change improves the skill>`

### Edit 2 — `<description>`

```diff
- <before>
+ <after>
```

**Rationale:** `<...>`

---

## Optional: handoff to skill-creator

If the user wants to verify these changes actually improve triggering or output quality (not just structure), suggest:

- **For description trigger rate:** hand off to `skill-creator` for the description-optimization loop (eval queries, 60/40 split, 3 runs per query).
- **For output quality:** hand off to `skill-creator` for the eval-driven iteration loop (test cases, baseline comparison, benchmark aggregation).

This skill optimizes the *artifact*; `skill-creator` measures the *outcome*.

---

## Approval checklist

Before applying changes, the user should confirm:

- [ ] All edits in the "Proposed edits" section look correct.
- [ ] The "Why this rewrite helps" notes make sense.
- [ ] No edits were silently dropped or changed from what was shown.
- [ ] The user understands that mechanical audit (Dimension 1) re-runs after edits; content audit (Dimensions 2–3) is manual.
