# Changelog / 变更日志

## Overview / 概述

代码修改→自检通过→测试通过后的最后一步：将改动写入项目变更日志。

Final step after code changes complete, self-check passes, and tests pass: write changes to project changelog. 支持自增长检测（发现重复Bug→自动升级规则）、反膨胀清理、一键分享导出。

## Write Format

Strictly follow this template, writing to `{{pipeline.paths.changelogFormat}}`:

```markdown
# Changelog - YYYY-MM-DD

## Change Summary
One sentence describing what was done (future-facing, explain "why")

---

## Changed Files

| File Path | Change Type | Brief Description |
|:--|:--|:--|
| `path/to/file.js` | Added/Modified/Deleted | Description |

---

## New Dependencies

None (or list package name + version)

---

## Self-Check Results Digest

| Check Item | Result |
|:--|:--|
| Architecture registration consistency | N/A / Passed |
| Schema field completeness | N/A / Passed |
| Truncation point scan | N/A / Passed |
| Numeric `\|\|` falsy check | N/A / Checked |
| `<select>` placeholder | N/A / Checked |
| POST upsert hardcoded values | N/A / Checked |
| Async race conditions | N/A / Checked |
| Lint | All passed |
```

## Workflow

### Step 0: Growth Detection (V2.1+)

**Before writing the changelog**, execute self-growth detection. See `references/growth-rules.md` for detailed rule definitions.

Execute `_detectGrowthOpportunity()`:

1. **Scan this session**: Review all `replace_in_file` / `write_to_file` operations
2. **Identify fix iterations**: Same file modified multiple times + bug fix signals ("fix", "bug", "error", "still broken")
3. **Extract bug pattern**: Distill general pattern from user feedback and fix content
4. **Match with observation pool** (`references/observations.md`):
   - Exists → confidence +1, record reoccurrence
   - Not exists → create new observation entry O-00X, confidence = 1
5. **Check promotion thresholds** (refer to `pipeline.json` `selfGrowth.confidenceThresholds`):
   - Confidence ≥ 3 → promote to [SOFT] rule, append to `self-check-full.md` auto-grown rules zone
   - Confidence ≥ 5 → promote to [HARD] rule
   - Record promotion event in `growth-log.md`
6. **Check retirement conditions**:
   - User rejected the rule suggestion during this session → confidence -2
   - Confidence drops to 0 → move to `retired.md`
7. **On completion**: Write "Growth Detection" entry in changelog summary

### Step 0.5: Anti-Bloat Check (V2.2+)

> **Why**: Without cleanup, rules accumulate indefinitely. A 6-month project can have 100+ rules, bloating every self-check. This step keeps the rule set lean.

Execute `_runAntiBloatCheck()` per `references/growth-rules.md` — **after growth detection, before changelog write**.

#### 1. Staleness Sweep (SOFT rules)

For each `[SOFT]` rule in `self-check-full.md`, check `growth-log.md` for `last_triggered`:
- If not triggered for N sessions (config: `softStalenessSessions`, default 10) → demote to observation pool, confidence reset to 1
- Log event in `growth-log.md`

#### 2. Hard Cap Enforcement

Count `[SOFT]` + `[HARD]` rules:
- If total > `maxTotalRules` (default 30): demote lowest-confidence `[SOFT]` rules until under cap
- If `[HARD]` > `maxHardRules` (default 15): demote lowest-confidence `[HARD]` → `[SOFT]` until under cap

#### 3. Observation Pool Pruning

- If observations > `maxObservations` (default 50): remove stale entries with confidence=1 and no re-trigger in 30 days
- If still over: remove lowest-confidence entries

#### 4. Retired Archives Compaction

- If retired > `retiredArchiveThreshold` (default 20): distill oldest 10 into a summary row

#### 5. Write Anti-Bloat Report

Append to changelog:

```
## Anti-Bloat Report (V2.2)

| Action | Details |
|:--|:--|
| Staleness sweep | N SOFT rules demoted |
| Hard cap enforcement | N rules demoted |
| Observation pruning | N old observations removed |
| Retired compaction | N retired entries distilled |
```

If no actions: "Anti-bloat check: rule set is within healthy limits."

### Step 1: Determine Date
Use current date, format `YYYY-MM-DD`.

### Step 2: Collect Info
- **Change summary**: User requirement + distilled change description
- **Changed file list**: git status or actual modification list
- **New dependencies**: npm install package names, "None" if empty
- **Self-check results**: Fill item by item from self-check output

### Step 3: Read/Write File
- File exists → `replace_in_file` append new change block
- File doesn't exist → `write_to_file` create new file
- Same day multiple changes: append to same file, separated by `---`

### Step 4: One-Click Share Export (V2.1+)

**Trigger**: When this session has Tier 2 [HARD] rules generated or promoted **AND** `shareContact.phone` is not empty.

**Before outputting**: Check `pipeline.json` → `selfGrowth.shareContact.phone`. If empty → skip this entire block.

Append share text block at end of changelog:

```
---
## 💡 Important Rules Auto-Discovered by AI

During this development session, the self-growing system discovered the following Tier 2 [HARD] rules:

> **[HARD] Rule Name**: Rule description
> Trigger: XXX
> Correct Pattern: XXX
> Confidence: N (consistently triggered N times)

---
These rules come from the **Vibe Coding Rules V2.2** self-growing system.
📱 Share: {{pipeline.selfGrowth.shareContact.phone}}
({{pipeline.selfGrowth.shareContact.projectName}})
```

**Format requirements**:
- Only list rules promoted or triggered as [HARD] this session
- One line per rule with brief description + confidence
- Phone and project name read from `pipeline.json` `selfGrowth.shareContact`
- **If phone is empty → skip this block entirely** (opt-in privacy design)
- If no [HARD] rule changes this session → skip regardless

### Step 5: Sync Overview Doc After Version Bump (V2.2+)

**When this change triggers a VERSION bump**, synchronize the project overview document (README.md / OVERVIEW.md):

1. Read project overview doc (check root `OVERVIEW.md` first, then `README.md`)
2. Search for version number references (patterns like `v1.0.0`, `version 1.0`)
3. If hardcoded version numbers exist → replace with new version
4. If overview doc references `.ai-pipeline/VERSION` → skip (already using best practice)
5. If project has no overview doc → skip

**Purpose**: Prevent churn — eliminate AI-generated zombie version numbers from inconsistent multi-file maintenance.

## Key Constraints

- **Write "why changed" not "what changed"**: Git tracks file changes, changelog tracks business reasons
- **Do not skip**: Must write after self-check + tests pass. No "I'll do it later."
