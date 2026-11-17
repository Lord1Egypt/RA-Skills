# Code Quality Reviewer — Shared Framework

**Single source of truth** for project config, report template, Health Score math, and opt-in history/triage.  
Risk symptom tables: `decay-risks.md`, `test-decay-risks.md`, `editorial-extensions.md`.  
Book grounding: `source-coverage.md` (Architecture / disputes only — not every Quick pass).

## The Iron Law

```
NEVER suggest fixes before completing risk diagnosis.
EVERY finding must follow: Symptom → Source → Consequence → Remedy.
Default: report only — edit code only on explicit fix / --fix.
```

## Project Config

Before review, try `.code-quality.yaml` at repo root. Missing → defaults (all risks on, `balanced`).

### Settings

- **`disable`** — skip risk codes (R1–R7, T1–T6, UX1).
- **`severity`** — force `critical` | `warning` | `suggestion` per code.
- **`ignore`** — glob exclude (e.g. `**/*.generated.*`).
- **`focus`** — only these codes; cannot combine with non-empty `disable`.
- **`strictness`** — `strict` | `balanced` (default) | `legacy-friendly`.
- **`history`** — `true` writes `.code-quality-history.json` trend; default `off` (see History Tracking).
- **`suppress`** — list of `{ id, reason, expires? }` from opt-in triage (see below).

```yaml
version: 1
strictness: balanced
disable: []
severity: {}
ignore:
  - "**/*.generated.*"
  - "**/node_modules/**"
suppress: []
history: false
```

### Validation

- Bad risk code / severity → skip that entry, note `Config warning: …`.
- Both `disable` and `focus` non-empty → ignore both, note error.
- Bad `strictness` → `balanced`.
- YAML parse fail → defaults.
- Expired `suppress` entries → ignore them (treat as active findings again).

If config applied, after **Scope**:  
`Config: .code-quality.yaml applied (strictness: …, N disabled, M ignored)`

## Auto Scope

- **PR:** `git diff --cached` → `git diff` → `git diff main...HEAD` (or `master`) → ask.
- **Architecture / debt:** whole project; `--since=<ref>` → modules of changed files only.
- **Test quality:** test files; prefer co-located with production diff.
- Always print `Scope: …`. Skip generated/lock/minified; note skips.

## Report Template (canonical)

User’s language for prose. English: Iron Law field labels, book titles, smell names, headers.

```markdown
# Code Quality Review

**Mode:** [Quick / PR Review / Architecture Audit / Tech Debt / Test Quality / Release Gate]
**Scope:** […]
**Health Score:** XX/100 *(per-run deduction index, not an absolute grade)*

[One-sentence verdict]

---

## Findings

### 🔴 Critical
**[Risk Name] — [Short title]**
Symptom: […]
Source: [Book — Principle or Smell | Editorial — R7/UX1]
Consequence: […]
Remedy: […]

### 🟡 Warning
… (same)

### 🟢 Suggestion
… (same)

---

## Summary
[2–3 sentences: highest-leverage action + trend if any]
```

Sort Critical → Warning → Suggestion. Omit empty tiers. If &gt; 5 findings, one-line **Recommended fix order**.

## Health Score

Base 100. Deduct by `strictness`:

| Preset | Critical | Warning | Suggestion |
|--------|----------|---------|------------|
| `strict` | −20 | −8 | −2 |
| `balanced` | −15 | −5 | −1 |
| `legacy-friendly` | −8 | −3 | −1 |

Floor 0. Still report every finding. Under `legacy-friendly`, Summary leads with three highest-leverage fixes.  
For aging codebases with no prior quality gate, prefer stating `legacy-friendly` in Scope when the user did not choose `strict`.

## Remedy Mode (opt-in)

Only if user says fix / `--fix`. Implement each Remedy as minimal behavior-preserving edits; re-review those findings; do not widen scope.

## History Tracking (opt-in)

**Default: off.** Enable only if user asks for history/trend, or `.code-quality.yaml` has `history: true`.

When enabled: append to `.code-quality-history.json`:  
`{ date, mode, score, findings: { critical, warning, suggestion }, scope }`.  
Prior same-mode run → `**Trend:** A → B (±N)`. First run → `First run — no trend data`.  
**Write failure:** print `History: skipped (reason)` — never invent a trend.

## Post-Report Triage (opt-in)

**Default: off.** Enable only if user says 「逐条处理」 / `--triage`, and the session is interactive (skip in CI/headless).

For Warning/Suggestion (lowest severity first): `[a]ccept / [d]ismiss / [f]defer / [s]kip`.  
- dismiss → `suppress: [{ id, reason }]`  
- defer → same + `expires: YYYY-MM-DD` (default +90 days)  
Do not block delivering the main report on triage.

## Reference routing

| File | When |
|------|------|
| `editorial-extensions.md` | Release gate; UI/splash; anti-over-flag disputes |
| `decay-risks.md` | Production findings needing severity/source |
| `test-decay-risks.md` | Test findings / PR Step 7 |
| `pr-review-guide.md` | Full PR process |
| `source-coverage.md` | Architecture / book tradeoffs |
| `examples.md` | Calibrate tone / score |
