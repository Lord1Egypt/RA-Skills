# Audit Report Output Template

## Scorecard Markdown File Template

Filename: `AUDIT-{YYYY-MM-DD}.md`
Location: the root directory of the audited skill

---

```markdown
# Skill Audit Report

| Field | Value |
|------|-----|
| Skill name | {skill-name} |
| Skill path | {skill-path} |
| Audit time | {YYYY-MM-DD HH:mm} |
| Check depth | L{1/2} ({static analysis / dryRun}) |
| Audit tool version | skill-deep-audit v{version} |

---

## Overall score: {score} / {max}　　{PASS ✅ / FAIL ❌}

> Max: L1 static 112 / L2 dryRun 115.
> Pass criteria (dual gate, both required): total ≥ pass line (L1/L2 dryRun both **≥90**) **and** zero ERR

---

## 🔴 ERR (must fix, {n} total)

> ⚠️ Any ERR means the audit result is FAIL, no matter how high the total score is.
> Every ERR must include the **four elements**: problem description / example (with line number) / fix (full code) / impact scope.

### [{ID}] {check name} (−{x} pts)

**① Problem**: {who, where, what problem, what it affects — one sentence capturing the essence}
**② Example**: `{file}` line {line}
```{lang}
{paste the specific offending code, marking the problem line}
```
**③ Fix**:
```{lang}
{the corrected full code snippet, noting where to change}
```
**④ Impact**: {other affected skills / files / callers; if none, write "this file only, no side effects"}

> ❌ A one-line description is not allowed — the reader must be able to locate and fix the issue from this entry.

---

## 🟡 WARN (recommended fixes, {n} total)

> WARN does not flip pass/fail by itself, but it lowers the total and may drop you below the pass line.
> WARN should also follow the four-element format (the "impact" element may be simplified).

### [{ID}] {check name} (−{x} pts)

**① Problem**: {specific description}
**② Example**: `{file}` line {line}: `{offending code}`
**③ Fix**: {suggestion / code snippet}
**④ Impact**: {affected scope}

---

## 📊 Per-dimension scores

| Dimension | Score | Max | ERR | WARN |
|------|------|------|-------|--------|
| D1 Process closure & idempotency | {d1} | 13 | {n} | {n} |
| D2 Tool & command conventions | {d2} | 10 | {n} | {n} |
| D3 Portability & defense | {d3} | 15 | {n} | {n} |
| D4 Skill usability | {d4} | 21 | {n} | {n} |
| D5 Security & operation risk | {d5} | 21 | {n} | {n} |
| D6 Code & doc quality | {d6} | 31 | {n} | {n} |
| D7 Dependency & footprint health | {d7} | 4 | {n} | {n} |
| **Total** | **{total}** | **115** | | |

---

## 🔮 Fix-path estimate

- Current score: {score} / {max}, with {n} ERR(s)
- Estimated score after fixing all ERRs: {estimated} / {max}
- Projected result after fixes: {PASS ✅ / still need to fix WARN to reach pass line ⚠️}
- Suggested fix priority: ERR (highest deduction first) → score-affecting WARN → remaining WARN

---

## 📋 Full check-item list

| ID | Check | Level | Pts | Depth | Result | Note |
|----|--------|------|------|---------|------|------|
| D1-E1 | Result verification after write op | ERR | 3 | L1 | {✅/❌/➖} | |
| D1-E2 | Pre-write completion check (idempotency) | ERR | 3 | L1 | | |
| D1-E3 | Exception branch halts the flow | ERR | 3 | L1 | | |
| D1-W1 | Execution summary at flow end | WARN | 2 | L1 | | |
| D1-W2 | Redundant op / no-op relay detection | WARN | 2 | L1 | | |
| D2-E1 | No raw HTTP/browser bypass of sensitive/controlled domains (configurable) | ERR | 3 | L1 | | |
| D2-W1 | Dynamic command-concat review | WARN | 3 | L1 | | |
| D2-W2 | Hardcoded URL review | WARN | 2 | L1 | | |
| D2-W3 | Cross-layer command-call tracing | WARN | 2 | L1 | | |
| D3-E1 | No hardcoded local absolute paths | ERR | 3 | L1 | | |
| D3-E2 | No hardcoded environment-specific constants | ERR | 3 | L1 | | |
| D3-E3 | No hardcoded column indexes | ERR | 3 | L1 | | |
| D3-W1 | No duplicated scripts across skills | WARN | 2 | L1 | | |
| D3-W2 | Branch-reachability simulation | WARN | 2 | L2 dryRun | ➖ skipped (dryRun item) | |
| D3-W3 | Actionable error messages | WARN | 2 | L1 | | |
| D4-E1 | frontmatter complete | ERR | 3 | L1 | | |
| D4-E2 | description states trigger timing | ERR | 3 | L1 | | |
| D4-E3 | Prerequisites documented | ERR | 3 | L1 | | |
| D4-E4 | Friendly message on missing required param | ERR | 3 | L1 | | |
| D4-E5 | Packaging-file hygiene | ERR | 3 | L1 | | |
| D4-W1 | Directory-structure conventions | WARN | 2 | L1 | | |
| D4-W2 | High-risk ops have guardrail declarations | WARN | 3 | L1 | | |
| D4-W3 | Progress feedback on key steps | WARN | 1 | L1 | | |
| D5-E1 | No plaintext sensitive credentials | ERR | 3 | L1 | | |
| D5-E2 | No hardcoded --yes/--force passthrough | ERR | 3 | L1 | | |
| D5-E3 | No hardcoded credentials in URLs | ERR | 3 | L1 | | |
| D5-W1 | Batch ops have an upper-bound guard | WARN | 3 | L1 | | |
| D5-W2 | Confirmation step before write ops | WARN | 3 | L1 | | |
| D5-W3 | Config-file plaintext-credential scan | WARN | 3 | L1 | | |
| D5-W4 | HTTP batch-write review | WARN | 3 | L1 | | |
| D6-E1 | Script syntax correct | ERR | 3 | L1 | | |
| D6-E2 | Logical completeness, no defects | ERR | 3 | L1 | | |
| D6-E3 | Key boundaries handled | ERR | 3 | L1 | | |
| D6-E4 | Description matches implementation | ERR | 3 | L1 | | |
| D6-E5 | SKILL.md-referenced required file paths exist | ERR | 3 | L1 | | |
| D6-E6 | Cross-table/cross-source field-format compatibility | ERR | 3 | L1 | | |
| D6-E7 | Format validation after parsing key columns | WARN | 3 | L1 | | |
| D6-W1 | Code completeness (no placeholders/TODO) | WARN | 2 | L1 | | |
| D6-W2 | Dependency tool versions declared | WARN | 2 | L1 | | |
| D6-W3 | SKILL.md-referenced non-required file path missing | WARN | 3 | L1 | | |
| D6-W4 | Large codebase lacks test coverage | WARN | 3 | L1 | | |
| D7-W1 | Published to hub | WARN | 1 | L2 dryRun | ➖ skipped (dryRun item) | |
| D7-W2 | Dependency skill list + attribution + existence | WARN | 2 | L1 extract + L2 existence | | |
| D7-W3 | Reasonable skill footprint | WARN | 1 | L1 | | |
```

---

## 🧩 False-positive & false-negative notes

> This section improves audit transparency, helping skill authors understand the tool's limitations.

### False positives — rule triggers but the skill is actually compliant

| Possibly triggered rule | Common false-positive scenario | How to appeal |
|------------|------------|---------|
| D5-E2 hardcoded `--yes` | Fully automated orchestration script with no TTY for interactive confirmation | Add an automation declaration in SKILL.md, see the D5-E2 exception notes |
| D1-W1 no execution summary | Single-step tool/query skill (not a batch pipeline) | Note the skill type as "tool/query" in SKILL.md |
| D5-W1 no batch cap | A guardrail declaration already exists in SKILL.md or the orchestration layer | Confirm the guardrail covers one of D5-W1's four criteria |
| D6-E4 description ≠ implementation | Steps use unconventional synonyms (e.g. "write back" for update) | Add a synonym note in SKILL.md, or make code naming match the steps |
| D7-W2 import misjudged as external dependency | An internal module/function of this skill is treated as an external skill | Use step ① of the "three-way join" algorithm to look it up inside this skill and exclude it |

### False negatives — rule does not trigger but a real problem exists

| False-negative scenario | Cause | Recommendation |
|---------|------|------|
| Dynamically concatenated high-risk command (`cmd = "tool " + user_input`) | String concat bypasses static pattern scanning | D2-W1 covers part of it; manually review dynamic command concat during code review |
| Indirect calls (subprocess.Popen runs shell, which calls another tool) | Cross-layer calls; static scan can't trace | D2-W3 + L2 branch-reachability simulation cover part; or manually review nested shell scripts |
| Soft-coded credentials (token sits in a plaintext sibling `config.json`) | D5-E1 only scans script assignment statements | D5-W3 already covers config-file scanning |

> **Summary**: static analysis has inherent limits. L2 dryRun fills part of the gap via read-only queries and branch-reachability simulation; for complex skills, manually review WARN items — especially the core write paths.

---

## 🔧 Section 5: Fix-suggestion block (end of report, supports one-click fix)

> The report always ends with this block, splitting all issues into two subsections by "can it be auto-fixed". Each item follows the four-element format above.
> The block must end by reminding the user: reply "fix" to start the one-click fix (see SKILL.md "One-click fix (`--fix`) behavior rules").

```markdown
## 🔧 Fix suggestions

{N+M} fixable issues this run, grouped by whether they can be auto-fixed.
⚠️ One-click fix modifies the audited skill's files; before starting it backs up the entire skill directory and reports the backup path.

### 5.1 ✅ Auto-fixable ({N} items — pure text/config/doc, no business-logic risk)

Applies to: adding frontmatter version, prerequisite notes, guardrail declarations, copy edits, dependency declarations, normalizing directory-reference prefixes, etc.

#### [{ID}] {check name}
- **① Problem**: {...}
- **② Example**: `{file}` line {line}: `{current content}`
- **③ Fix**: `{new content}`
- **④ Impact**: {file} only, no business-logic side effects

### 5.2 ⚠️ Needs manual confirmation ({M} items — touches business logic/script code, requires human review)

Applies to: changing script control flow, field-matching logic, HTTP call style, column-name mapping, removing over-privileged steps, etc.

#### [{ID}] {check name}
- **① Problem**: {...}
- **② Example**: `{file}` line {line} (paste code snippet)
- **③ Fix**: {full corrected code snippet}
- **④ Impact**: {affected skills/files/callers}
- ⚠️ **Why manual confirmation**: {touches business logic; auto-changing may introduce regressions; needs developer review + testing}

---

> 💡 Reply "fix" to start the one-click fix (handles 5.1 only); each 5.2 item is changed only after you confirm it individually.
> The skill directory is backed up before any fix; after fixing you'll be asked whether to re-audit.
```

---

## 📦 Section 6: Skill-dependencies section (fixed report section)

> The report always outputs this section, stating clearly **which skills the audited skill depends on, what it uses them for, and whether they are installed**.
> Always output this section no matter how many dependencies (even 0); for 0, write "✅ This skill has no external skill dependencies".

```markdown
## 📦 Skill dependencies

This skill depends on the following {n} external skill(s):

| Dependency skill | What it's used for | Reference style | Status |
|-----------|------------|---------|------|
| some-skill | {purpose} | subprocess calls xxx.sh | Installed locally ✅ |
| other-skill | {purpose} | from xxx import yyy | On hub, not installed ⚠️ |
| missing-skill | {purpose} | {import / subprocess / CLI} | Not found ❌ |

**Status legend**:
- ✅ Installed locally: `<skills-dir>/<dep>/` exists
- ⚠️ On hub, not installed: absent locally, but found on the skill hub
- ❌ Not found: absent locally + not on hub → **ERR**, needs manual review (typo in name? private skill? deprecated?)
```
