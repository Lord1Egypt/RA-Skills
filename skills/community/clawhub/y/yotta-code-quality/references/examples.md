# Examples — tone and score calibration

Use these to keep reviews consistent. Do **not** copy findings into real reports unless the code matches.

---

## Example A — Good Warning (R2)

**Context:** PR renames a domain field and also “cleans up” unrelated formatting in 12 files.

```
### 🟡 Warning
**Change Propagation — Unrelated drive-by edits**
Symptom: Diff touches 12 files; only 2 mention the renamed field `expires_at`; the rest are import reorder / whitespace.
Source: Fowler — Refactoring — Shotgun Surgery / Divergent Change
Consequence: Reviewers cannot see the real contract change; regressions hide in noise; blame history is polluted.
Remedy: Split into (1) rename + call sites, (2) optional format-only PR — or revert non-functional hunks.
```

**Score impact (balanced):** −5.

---

## Example B — Over-flag to avoid (R1)

**Bad:** Mark a 80-line React component Critical solely because `function > 20 lines`, when it is mostly JSX layout with one `map`.

**Better:** No finding, or Suggestion: extract presentational subcomponents *when editing nearby* — Source Editorial / Code Complete heuristics as hints.

---

## Example C — Editorial Critical (R7)

```
### 🔴 Critical
**Release / Supply-chain Safety — Plaintext cloud credentials in publish script**
Symptom: `publish-*.ps1` embeds AccessKeyId/Secret as string literals committed to the repo.
Source: Editorial — Release Safety
Consequence: Anyone with repo (or old clone) access can abuse the cloud account; rotation is urgent.
Remedy: Remove secrets from VCS history of the file; load from env / local config ignored by git; rotate keys in the provider console now.
```

**Score impact (balanced):** −15.

---

## Example D — Health Score arithmetic

Findings: 1 Critical, 2 Warning, 1 Suggestion; `strictness: balanced`.  
`100 − 15 − 5 − 5 − 1 = 74` → **Health Score: 74/100**.

Disclaimer in report: per-run deduction index, not “the project is 74% healthy.”

---

## Example E — Quick mode depth

User pastes a 30-line function. **Do not** load all of `source-coverage.md`.  
Use SKILL cheat-sheet; open `decay-risks.md` only if you are about to emit Critical.
