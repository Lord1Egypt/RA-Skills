# Post-Code-Change Self-Check V2.5 / 代码修改后自检 V2.5

## Overview / 概述

每次代码修改后的强制自检流程。逐项遍历 28 条规则，防止重复已知 Bug 模式。V2.5 新增面包屑自动播种——每次文件修改自动植入 AI 导航面包屑。

Mandatory self-check process after every code change. Iterates through 28 rules item by item to prevent repeating known bug patterns. V2.5 adds breadcrumb auto-seeding — every file change automatically plants AI-navigable breadcrumbs.

## Trigger Conditions (read from pipeline.json)

**Must execute** when any of the following occurs:

- {{#if hasToolDirectory}}Modifying files in `{{pipeline.architecture.toolDirectory}}`{{/if}}
- Modifying tool schema (name/description/parameters)
- {{#if hasThreeLayerRegistration}}Modifying `{{pipeline.architecture.fallbackToolsConstant}}` fallback list{{/if}}
- Modifying core task-link code
- {{#if hasDualEntry}}Modifying dual-entry HTML files{{/if}}
- Modifying Express routes
- Modifying database schema

## Self-Check Workflow / 自检流程

### Step -1: Pre-Modification Anchor Scan (V2.4+)

**Before writing any code**, scan target files for existing anchors (executed in coding-principles Principle 0):

1. **Scan @COUPLED tags**: record all coupled file paths → add them to self-check scope
2. **Scan 📖 references**: record all referenced docs → read their "Implementation Location" sections
3. **Scan 🍞 breadcrumb header**: if file has 🍞 block → parse @COUPLED/📖/@GOTCHA/@BUGFIX for navigation context
4. **If no 🍞 header**: mark "this file needs breadcrumb seeding after changes"

### Step 0: Locate Rules by Code Type Changed

Based on what you changed, use the index to locate relevant rules. See `references/self-check-full.md` Section 0. You don't need to iterate all 28 rules — only check rules triggered by your change type.

Quick index reference:

| What Changed | Required Rules | Extra Checks |
|-------------|----------------|-------------|
| New/modified tool | 5,6,7,14,28 | Schema completeness + truncation + breadcrumb |
| Tool registration/fallback list | 5,6,28 | Full diff + breadcrumb |
| Data transport pipeline | 5,6,7,28 | Truncation full scan + breadcrumb |
| Frontend core JS | 8,9,14,28 | Breadcrumb |
| Frontend workflow JS | 8,9,12,16,17,18,19,20,28 | All close paths + breadcrumb |
| Modal/popup/overlay | 12,28 | Exhaust close paths + breadcrumb |
| CSS/layout | 16,28 | Check adjacent components + breadcrumb |
| Express routes | 13,24,26,27,28 | Fixed-before-param + breadcrumb |
| Middleware | 28 | Manual: try/catch empty body + breadcrumb |
| Database schema/migration | 10,28 | Migration numbering + breadcrumb |
| Core library (LLM/payment/WS) | 23,28 | ESM/CJS compat + breadcrumb |
| Shared modules | 23,28 | ESM/CJS dual-format + breadcrumb |
| Desktop main process | 28 | Manual: IPC channels/window lifecycle + breadcrumb |

### Step 0.6: Breadcrumb Auto-Seeding 🍞 (V2.5 NEW — Mandatory for Every File Changed)

> Breadcrumbs are the AI's project map. This step ensures every code change automatically plants breadcrumbs, so any future AI opening the same file can navigate without extra context.

For **every modified file**:

**A. File has NO 🍞 header → Create one**:
Insert the standard 🍞 navigation block at the file header (after `'use strict'`, before first `import/require`):

```
/*
 * ─── 🍞 AI Breadcrumb Navigation ──────────────────
 * Tag meanings: @COUPLED=linked files @GOTCHA=gotcha @BUGFIX=bug fix @MAGIC=magic number
 *              @DEPENDS=external dependency @ASSUME=assumption @TODO=todo @WHY=design rationale
 *              @PERF=performance @CONTRACT=interface contract 📖=dev doc reference
 * 
 * Breadcrumbs (changing this affects):
 *   @COUPLED sync needed: fileA, fileB
 *   📖 see: docs/xxx/yyy.md
 * ──────────────────────────────────────────────────
 */
```

Auto-fill breadcrumbs detected during this change:
- a) **`@COUPLED`**: which other files were modified in this session? → mutual cross-reference
- b) **`📖`**: which dev docs were read during this change? → link them
- c) **`@BUGFIX`**: is this a bug fix? → add date + reason + solution
- d) **`@GOTCHA`**: any counter-intuitive patterns? → mark the trap
- e) **`@MAGIC`**: any hardcoded business numbers? → annotate meaning

**B. File already HAS 🍞 header → Update it**:
1. Verify existing `@COUPLED` file paths still exist
2. Verify existing `📖` doc paths still exist
3. Add new breadcrumbs from this change
4. Remove/stale-mark expired breadcrumbs

**C. Breadcrumb quality requirements** (block if violated):
- `@COUPLED` must specify file paths (or file+line), NOT vague "all frontend files"
- `📖` must point to real existing documents → block if missing
- `@BUGFIX` must include date + brief reason + fix approach

**D. Insertion position rules by language**:
- JavaScript/TypeScript: after `'use strict';`, before first `import/require`
- HTML: after `<!DOCTYPE html>`, before `<head>` (use `<!-- -->` comments)
- CSS: first line (use `/* */` comments)
- Python: after `#!` shebang, before first `import` (use `#` lines, replace 🍞 with `[breadcrumb]`)
- Markdown: after `#` title, before body text (use `<!-- -->` HTML comments)

**Why this format is AI-readable without any external docs**:
- `🍞` emoji = visual anchor, AI can `grep /🍞/` to locate instantly
- Tag meanings line = **inline cheat sheet**, no need to read ANCHOR_SPEC.md
- `@COUPLED` + file list = tells AI exactly which files to change together
- `📖` + doc path = entry point to detailed design docs
- `@BUGFIX` + date = prevents regressions

This step ensures: **every code change = one breadcrumb planted automatically**. No manual effort needed.

### Step 1: Architecture Registration Check (optional, per pipeline.json config)

{{#if hasThreeLayerRegistration}}
Check consistency between `{{pipeline.architecture.toolDirectory}}` and `{{pipeline.architecture.fallbackToolsConstant}}`.
Confirm count is `{{pipeline.architecture.toolCount}}`.
{{else}}
Skip (project `pipeline.json` has `architecture.hasThreeLayerRegistration` = false)
{{/if}}

### Step 2: Schema Field Completeness (if tools involved)

Confirm each tool entry has complete `name`/`description`/`parameters`.

### Step 3: Implementation Location Cross-Validation (V2.4+ — Four-Hop Chain)

If this change involves **dev docs** or **code referenced in docs' "Implementation Location"**:

1. **Changed docs** → verify "Implementation Location" sections are still accurate
2. **Changed code** → search which docs' "Implementation Location" references this file → check if they need updates
3. **📖 bi-directional verification**:
   - Code 📖 path → doc exists?
   - Doc "Implementation Location" → code path exists?
   - Either broken → fix or mark (block if path missing, warn if content mismatch)

### Step 4: Truncation Point Scan (if data transport involved)

{{#if hasTruncationPoints}}
Check all configured truncation points:
{{#each pipeline.architecture.truncationPoints}}
- `{{this}}`
{{/each}}
Confirm truncation limits can accommodate maximum data volume.
{{else}}
Skip (no truncation points configured)
{{/if}}

### Step 5: Iterate Through 28 Rules

Select relevant rules by change type. Core rule quick reference:

| Rule | Core | Trigger |
|------|------|---------|
| 8 | No `\|\|` for numeric falsy checks | Frontend JS changes |
| 9 | `<select>` must have placeholder option | Form/dropdown changes |
| 10 | POST upsert must not hardcode fields | Backend route changes |
| 11 | Rule self-growth | Fixed a new type of bug |
| 12 | Overlay must exhaust all close paths | Modal/drawer/overlay |
| 13 | Fixed routes before parameterized routes | Express routes |
| 14 | New tool → add to frontend display-name map | Tool addition |
| 16 | Layout migration: reset old artifacts | CSS/layout refactor |
| 18 | Re-initializable container: sync children | innerHTML rebuild |
| 20 | Async callback: verify context consistency | fetch/async |
| 23 | npm dep: check ESM/CJS compatibility | New dependency |
| 24 | GET/POST same-API data source symmetry | Route changes |
| 26 | Intent anchor comments (V2.3) | Any code change |
| 27 | Code-doc linkage consistency (V2.3) | Code references doc paths |
| 28 | 🍞 Breadcrumb auto-seeding (V2.5) | Any code change |

### Step 6: Historical Incident Pattern Match

Think: Could this change reproduce a known incident pattern? Reference `references/incident-history.md`.

### Step 6.5: Trust-Tiered Rule Check (V2.1+)

> This step handles self-growing system generated Trust-Tiered rules. Only executes when project `.ai-pipeline/` exists.

1. **Read observation pool**: `read_file("references/observations.md")`
   - Check if any Tier 0 observation entries relate to this change
   - If related, record "this pattern has been observed N times before"

2. **Read auto-grown rules**: Check `[SOFT]` and `[HARD]` marked rules at the end of `self-check-full.md` in the [Auto-Grown Rules Zone]
   - `[HARD]` rules → mandatory block, must fix
   - `[SOFT]` rules → warn, suggest fix but skippable

3. **User resistance demotion**: If user explicitly says "ignore this rule" or "skip this":
   - Record demotion event in `growth-log.md`
   - `[HARD]` → demote to `[SOFT]` (confidence -2)
   - `[SOFT]` → demote back to `observations.md` observation pool (confidence -2)
   - Confidence hits 0 → move to `retired.md`

4. **Retired rule check**: `read_file("references/retired.md")`
   - If current change pattern matches a retired rule, do NOT alert again

5. **Rule bloat sanity check (V2.2)**: Quick count of active rules
   - Count `[SOFT]` + `[HARD]` rules in `self-check-full.md`
   - If total > `antiBloat.maxTotalRules` (default 30): warn user
   - If `[HARD]` > `antiBloat.maxHardRules` (default 15): same warning

### Step 7: Automated Testing (optional)

{{#if pipeline.skills.webTesting.enabled}}
After self-check passes, execute automated tests:
- Check if project `{{pipeline.paths.tests}}` has test scripts
- Run tests and confirm all pass
{{else}}
Skip (webTesting not enabled in pipeline.json)
{{/if}}

### Step 8: Changelog (mandatory)

After self-check + tests all pass, record this change:
- Format: change summary → file list → new deps → self-check digest
- Write to `{{pipeline.paths.changelogFormat}}`
- Must NOT skip or "do it later"

## Related Skill Orchestration

```
coding-principles (pre-code check + breadcrumb pre-scan 🍞 V2.5)
    ↓
safe-terminal-executor (if API verification needed)
    ↓
self-check (post-code check) ← This Skill
    ├── Step -1: pre-modification anchor scan
    ├── Step 0: locate rules by code type
    ├── Step 0.6: 🍞 breadcrumb auto-seeding (V2.5)
    ├── Step 1-2: architecture diff + schema
    ├── Step 3: implementation cross-validation (four-hop chain)
    ├── Step 4: truncation point scan
    ├── Step 5: iterate 28 rules
    ├── Step 6: incident pattern match
    ├── Step 6.5: trust-tier check
    ↓
web-testing (automated testing, optional)
    ↓
changelog (change log)
    ↓
git commit
    ↓
Delivery closed loop
```

## Resources

- `references/self-check-full.md` — Complete self-check document (28 rules + auto-grown zone + V2.5 four-hop chain + 🍞 breadcrumbs)
- `references/incident-history.md` — Historical incident root cause + lesson quick reference
- `references/observations.md` — Tier 0 observation pool (V2.1+)
- `references/retired.md` — Retired rules archive (V2.1+)
- `references/growth-log.md` — Growth event log (V2.1+)
