---
name: skill-deep-audit
description: >
  Generic skill-quality auditor for any agent skill (Claude, OpenClaw,
  Cursor, etc.). Runs a 7-dimension static analysis (D1 process closure
  & idempotency, D2 tool/command conventions, D3 portability & defense,
  D4 skill usability, D5 security & op risk, D6 code & doc quality, D7
  dependency & footprint) with explicit ERR / WARN severity, 115-point
  scoring (pass line 90 + zero ERR), and an opt-in `--fix` workflow that
  always backs up first. Two depths: L1 static (~2 min) and L2 dryRun
  (~5 min, read-only hub + reachability checks). Strict red lines —
  read-only by default, never executes the audited skill's writes.
  Use when the user asks to "audit a skill", "check skill quality",
  "is this skill ready to ship", "lint my skill", or runs this tool by
  name. Triggers also: "审计这个 Skill"、"检查 Skill 质量"、"Skill 能上线吗"、
  "skill-deep-audit"、"审一下 xxx skill"。
---

# skill-deep-audit — Generic Skill Auditor

A read-only, multi-dimensional quality auditor for agent skills. Runs static
analysis + optional dryRun reachability checks and produces a scorecard.

- **Version**: 1.0.3
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/build-better-skills
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

## Design principles

```
Can it run?            → D3 Portability + D4 Usability conventions
Does it run correctly? → D1 Process closure + D6 Code & doc quality
Is it safe to run?     → D5 Security & op risk
Is it well-conformed?  → D2 Tool & command conventions
Is the whole healthy?  → D7 Dependency & footprint
```

## NEVER DO

- Do **not** execute any write operation of the audited skill (read-only,
  reachability checks, and static analysis only).
- Do **not** modify the audited skill's files (read-only and report-only;
  `--fix` is the one exception and requires explicit user authorization).
- Do **not** fabricate check results — when undecidable, mark
  "cannot confirm, manual verification needed".

## MUST DO

- At the start of every audit, **ask the user to choose the check depth
  (L1 / L2 dryRun) and wait** for the choice.
- Any ERR → final result is FAIL, regardless of total score.
- After the audit, **write the scorecard MD file**.
- If an L2 dryRun check fails because an external dependency is
  unavailable, **downgrade to WARN** with the reason — do not abort.

---

## Dependencies of this skill (all soft — degrade gracefully if missing)

| Dependency | Purpose | Behavior if missing |
|-----------|---------|---------------------|
| A skill-hub query tool (e.g. `clawhub`) | Hub publish-status check (D7-W1) and dependency existence check (D7-W2 step 3) | Skip Hub checks, related items downgrade to WARN, do not abort the audit |

> The core of this skill is pure static / read-only analysis. **There are no
> hard external dependencies** — L1 static audit works even if no tooling is
> installed.

---

## Step 0: Ask for check depth

At the start of the audit, present the following options and **wait for the
user to choose explicitly**:

```
Please choose check depth:

L1 Static analysis (~2 min)
   File read, structural check, keyword scan, syntax check.
   Max 112 (skips items that need to touch external systems). Pass line ≥ 90.
   Good for: quick first-draft check.

L2 dryRun (~5 min, recommended) ⭐
   L1 + Hub existence check + dependency existence check + branch reachability
   simulation (file existence / env config / read-only verification of
   unhit branches).
   Max 115. Pass line ≥ 90.
   Good for: pre-release / pre-ship full acceptance.

Default recommendation: L2 dryRun. Reply 1 / L1 for static, 2 / L2 for dryRun
(empty Enter = L2).

⚠️ Note: L2 dryRun does ONLY read-only queries and reachability checks. It
   performs no writes / updates, and it does NOT actually run the audited
   skill's business workflow.
```

---

## Step 1: Locate the skill directory

The user may provide:
- A skill name (e.g. `my-skill`) → look for a same-named folder under
  `<skills-dir>/`. `<skills-dir>` is the agent's skills directory and may be
  e.g. `~/.claude/skills/`, `~/.openclaw/workspace/skills/`, or any path the
  user specifies. Some agents use a different layout — adjust to what's actually
  on disk.
- A relative or absolute path (e.g. `skills/my-skill/`) → use directly.

```bash
ls {skill-path}/
cat {skill-path}/SKILL.md | head -20
```

If the directory cannot be found → tell the user and stop. Do not guess.

---

## Step 2: Static analysis (runs at every depth)

Execute each check defined in
[references/check-rules.md](./references/check-rules.md) in order.

> ⚖️ **Determinism guarantee**: each rule's hit/miss decision uses the grep
> pattern, keyword list, and numeric thresholds defined for it in
> check-rules.md — **not** the agent's subjective judgement. Edge cases not
> explicitly covered by a rule are handled by the "False-Positive General
> Rules" section (marked "manual verification needed", not hard-judged). This
> guarantees stable, repeatable results across different agents / re-runs.

### 2.1 Collect file list

```bash
# Script extensions must cover mixed-language skills — .js/.cjs/.mjs/.ts cannot be missed
find {skill-path} -type f \( \
  -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" -o -name "*.yaml" \
  -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) \
  | grep -v __pycache__ | grep -v node_modules | grep -v .git
```

> ⚠️ **Extension coverage blind-spot**: `find -name "*.js"` does **not** match
> `.cjs` / `.mjs` / `.ts`. Python scripts often `subprocess`-call a sibling
> `xxx.cjs` — if the file list misses `.cjs`, the auditor will wrongly report
> "called script does not exist" (false positive on D6-E4 / D6-E6). All later
> extension-scoped scans must include the full set.

### 2.2 Per-dimension static scan

Execute in order: **D1 → D2 → D3 → D4 → D5 → D6**.

> ℹ️ **D7 is not in this step**: D7 (dependencies & footprint) needs the code
> stats (see 2.4) plus Hub / existence checks, so it is consolidated into
> **Step 4**. Step 2 only scans D1–D6.

**Execution-level convention**:
- Rule title contains `L1` → runs at all depths.
- Rule title contains `L2 dryRun` → runs only at L2 dryRun; for L1, mark as
  `➖ skipped (L2 dryRun item)`.
- **D4-E5 scan must exclude** `{skill-path}/AUDIT-*.md` — audit reports are
  produced by this tool itself and are not part of the audited skill's package.

For each rule:
1. Check whether its execution level matches the current depth; if not,
   record ➖ skipped.
2. Run the corresponding scan command (grep / regex / file parse /
   agent-read judgement).
3. Record: pass ✅ / fail ❌ / skipped ➖.
4. Accumulate deductions.

### 2.3 D6-E1 script syntax check

```bash
# Python
for f in $(find {skill-path}/scripts -name "*.py" 2>/dev/null); do
  python3 -m py_compile "$f" 2>&1 && echo "OK: $f" || echo "SYNTAX ERR: $f"
done

# Shell
for f in $(find {skill-path}/scripts -name "*.sh" 2>/dev/null); do
  bash -n "$f" 2>&1 && echo "OK: $f" || echo "SYNTAX ERR: $f"
done
```

### 2.4 Code-size stats (prerequisite for D7)

```bash
# Number of script files (covers mixed skills: .js/.cjs/.mjs/.ts)
find {skill-path}/scripts -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) 2>/dev/null | grep -v node_modules | wc -l

# Total line count (-r prevents hang on no-match)
find {skill-path} \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) | grep -v node_modules | xargs -r wc -l 2>/dev/null | tail -1

# Skill-on-skill dependency: precise extraction (see D7-W2 "three-step join" algorithm)

# ① List all suspicious import candidates (just module names; ownership is resolved later)
grep -rnE "^\s*(from [a-zA-Z_][a-zA-Z0-9_]* import|import [a-zA-Z_][a-zA-Z0-9_]*)" {skill-path}/scripts/ 2>/dev/null
# ① supplementary: look for sys.path injection / skill_root concatenation
#    (this is the physical evidence of which skill an import belongs to)
grep -rnE "sys\.path\.insert.*skills/|_skill_root|skills/[a-z-]+/scripts" {skill-path}/scripts/ 2>/dev/null

# ② subprocess calls into other skills' scripts (by path)
grep -rnE "skills/[a-z-]+/scripts|_skill_root.*scripts" {skill-path} 2>/dev/null | grep -v __pycache__
# ③ Explicit declaration in SKILL.md
grep -nE "metadata.*requires|depends on .* skill|requires the .* skill|use .* skill" {skill-path}/SKILL.md 2>/dev/null
# → Agent then deduplicates, applies the three-step join to fix ownership, annotates purpose,
#   runs the existence check (D7-W2), and writes the result into report section
#   "VI. Skill Dependencies".
# → Stdlib and well-known PyPI packages (os/sys/json/re/requests/openpyxl …) are excluded
#   from ownership judgement.
```

---

## Step 3: Hub existence check (runs at L2 dryRun)

> **Pre-check**: this step requires a skill-hub query tool (e.g. `clawhub`).
> If unavailable → skip Hub checks; mark D7-W1 as "cannot verify (no hub
> tooling)", downgrade to WARN, do not abort.

1. Extract the `name` field from frontmatter.
2. Use the available skill-hub query tool to check whether the skill is
   already published.
3. Record the result against D7-W1 (not published → WARN, not ERR).

---

## Step 4: Dependency & footprint analysis (D7)

- **D7-W1** Hub publish status (consolidated from Step 3).
- **D7-W2** Precise dependency-skill list + purpose annotation + existence
  check (local ✅ / hub-has-not-installed ⚠️ / not-found ❌). Output a
  full list in report section "VI. Skill Dependencies" regardless of count;
  ≥ 5 deps → WARN; depending on a "not found ❌" skill → ERR; depending on a
  "hub-has-not-installed ⚠️" skill → WARN.
- **D7-W3** Code ≥ 5000 lines or scripts ≥ 10 → identify high-cohesion
  modules and suggest a split direction.

---

## Step 5: Aggregate scoring

**Total 115 points**

| Dimension | Max |
|-----------|-----|
| D1 Process closure & idempotency | 13 |
| D2 Tool & command conventions | 10 |
| D3 Portability & defense | 15 |
| D4 Skill usability conventions | 21 |
| D5 Security & op risk | 21 |
| D6 Code & doc quality | 31 |
| D7 Dependency & footprint health | 4 |
| **Total** | **115** |

> 📊 **Scoring convention**: ERR is uniformly 3 points (a hit means FAIL; the
> point value carries no real meaning). WARN uses three priority tiers
> (high 3 / mid 2 / low 1) — the difference is meant to guide fix order.

**Dual-judgement (both conditions must hold for PASS)**:

Pass line is uniformly 90 at both depths (skipped items don't count toward
the actual max but don't change the pass line):

| Depth | Actual max | Pass line |
|-------|-----------|-----------|
| L1 static | 112 | **≥ 90** |
| L2 dryRun | 115 | **≥ 90** |

| Condition | Result |
|-----------|--------|
| Total ≥ pass line **AND** zero ERR | ✅ **PASS** |
| Any ERR, **OR** total < pass line | ❌ **FAIL** |

---

## Step 6: Produce the scorecard MD file

Generate the full report using
[references/output-template.md](./references/output-template.md).

Write path: `{skill-path}/AUDIT-{YYYY-MM-DD}.md`

> `AUDIT-*.md` should not be packaged with the skill (D4-E5 will detect this).

---

## Step 7: Output summary

```
📋 Audit complete: {skill-name}
─────────────────────────────────────
Total score: {score}/{max}   {PASS ✅ / FAIL ❌}  (L1 max 112 / L2 dryRun max 115)
Pass line:   ≥ 90 (uniform across L1 / L2 dryRun)  AND  zero ERR (dual-judgement)
Depth:       {L1 static / L2 dryRun}

🔴 ERR: {n}   |   🟡 WARN: {n}
Highest-priority fix: {ID and name of the highest-deduction ERR}

Estimated score after fixing all ERR: {estimated}/{max}

📁 Scorecard: {skill-path}/AUDIT-{date}.md

🔧 Fix: {N} items auto-fixable / {M} items need human confirmation
   Reply "fix" to start auto-fix (the skill folder is backed up first).
```

---

## Step 8: Auto-fix (`--fix`) behavior spec

> ⚠️ **This is the only step in skill-deep-audit that is allowed to modify
> the audited skill's files**, and only after **explicit user
> authorization**. The day-to-day audit (Step 0–7) strictly observes the
> "audit-only, never fix" red line.

### Trigger conditions

- The user explicitly replies "fix", "apply fix", "`--fix`", "fix 5.1", etc.
  after the report is delivered.
- **Without explicit user authorization, never auto-fix.** The report only
  *recommends*; it does not *execute*.

### Fix scope tiers (corresponds to report section "V. Fix Recommendations")

| Sub-section | Type | Auto-fix? |
|-------------|------|-----------|
| **5.1 Auto-fixable** | Pure text / config / docs (add `version`, add prerequisites, edit wording, add dependency declaration, normalize reference prefixes — no business logic) | ✅ User says "fix" → batch apply |
| **5.2 Needs human confirmation** | Business logic / script code (change control flow, change field matching, change HTTP call, change column mapping, remove over-privileged steps) | ⚠️ Must confirm each item with the user; user approves one → fix one |

### Execution flow (strict order)

1. **Mandatory pre-fix backup**:
   - Copy the entire audited skill directory to a backup path:
     `{skill-path}.bak-{YYYYMMDD-HHMMSS}`
   - **Immediately tell the user the full backup path.**
   - If backup fails → abort the fix, don't touch anything.
   ```bash
   BACKUP="{skill-path}.bak-$(date +%Y%m%d-%H%M%S)"
   cp -r "{skill-path}" "$BACKUP" && echo "✅ Backed up to $BACKUP"
   ```

2. **Apply fixes item by item**:
   - 5.1 items: edit directly per the report's "③ Fix" section. After each
     change, briefly report `✅ Fixed [ID]`.
   - 5.2 items: only change after the user explicitly confirms that item;
     items the user hasn't approved are not touched.

3. **Do not auto-re-audit**:
   - After fixes, **prompt the user**:
     `🔧 Fixed {n} items. Re-run the audit now to verify? (reply "re-audit" to start)`
   - **Wait for the user to confirm "re-audit"** before re-running Steps 0–7.

4. **Fix record**: in the report or reply, list "which files / which items
   were changed + backup path" so the user can roll back.

### Red lines (also apply during fix)

- Do not execute any write operation.
- Do not delete any file (even if it looks redundant); if deletion is needed
  ask the user separately.
- 5.2 business-logic items are **never** changed unilaterally, even if they
  "look safe".
- If the user wants to roll back after fix: instruct the user to restore by
  copying the backup directory over.

---

## Part of build-better-skills

This skill belongs to the [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite.
For the full lifecycle map (Install → Audit → Release → Testing → Sediment),
all sibling skills, and their current status, see the
[**Stages table**](https://github.com/Songhonglei/build-better-skills#stages) on the suite repo home — kept as the single source
of truth (this file does not duplicate it).

## Rule references

- Full rule decision logic → [references/check-rules.md](./references/check-rules.md)
- False-positive / boundary general rules → [references/check-rules.md "False-Positive General Rules" section](./references/check-rules.md)
- Controlled-domain config (D2-E1, default empty) → [references/controlled-domains.md](./references/controlled-domains.md)
- Report MD template → [references/output-template.md](./references/output-template.md)
