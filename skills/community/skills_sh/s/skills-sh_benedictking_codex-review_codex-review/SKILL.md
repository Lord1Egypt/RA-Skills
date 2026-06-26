---
name: codex-review
version: 2.1.9
author: BenedictKing
description: "Professional code review skill for Claude Code. Automatically collects file changes and task status, and proactively fixes P0/P1/P2 issues after review. Triggers when working directory has uncommitted changes, or reviews latest commit when clean. Triggers: code review, review, 代码审核, 代码审查, 检查代码"
allowed-tools:
  - Task
  - Bash
  - Read
  - Glob
  - Write
  - Edit
user-invocable: true
---

# Codex Code Review Skill

## Trigger Conditions

Triggered when user input contains:

- "代码审核", "代码审查", "审查代码", "审核代码"
- "review", "code review", "review code", "codex 审核"
- "帮我审核", "检查代码", "审一下", "看看代码"

## Core Concept: Intention vs Implementation

Running `codex review --uncommitted` alone only shows AI "what was done (Implementation)".
Recording intention first tells AI "what you wanted to do (Intention)".

**"Code changes + intention description" as combined input is the most effective way to improve AI code review quality.**

## Skill Architecture

This skill operates in two phases:

1. **Preparation Phase** (current context): Check working directory, update CHANGELOG
2. **Review Phase** (isolated context): Invoke Task tool to execute Lint + codex review (using context: fork to reduce context waste)

## Execution Steps

### 0. [First] Check Working Directory Status

```bash
git diff --name-only && git status --short
```

**Decide review mode based on output:**

- **Has uncommitted changes** → Continue with steps 1-4 (normal flow)
- **Clean working directory** → Directly invoke codex-runner: `codex review --commit HEAD`

### 1. [Mandatory] Check if CHANGELOG is Updated

**Before any review, must check if CHANGELOG.md contains description of current changes.**

```bash
# Check if CHANGELOG.md is in uncommitted changes
git diff --name-only | grep -E "(CHANGELOG|changelog)"
```

**If CHANGELOG is not updated, you must automatically perform the following (don't ask user to do it manually):**

1. **Analyze changes**: Run `git diff --stat` and `git diff` to get complete changes
2. **Auto-generate CHANGELOG entry**: Generate compliant entry based on code changes
3. **Write to CHANGELOG.md**: Use Edit tool to insert entry at top of `[Unreleased]` section
4. **Continue review flow**: Immediately proceed to next steps after CHANGELOG update

**Auto-generated CHANGELOG entry format:**

```markdown
## [Unreleased]

### Added / Changed / Fixed

- Feature description: what problem was solved or what functionality was implemented
- Affected files: main modified files/modules
```

**Example - Auto-generation Flow:**

```
1. Detected CHANGELOG not updated
2. Run git diff --stat, found handlers/responses.go modified (+88 lines)
3. Run git diff to analyze details: added CompactHandler function
4. Auto-generate entry:
   ### Added
   - Added `/v1/responses/compact` endpoint for conversation context compression
   - Supports multi-channel failover and request body size limits
5. Use Edit tool to write to CHANGELOG.md
6. Continue with lint and codex review
```

### 2. [Critical] Stage All New Files

**Before invoking codex review, must add all new files (untracked files) to git staging area, otherwise codex will report P1 error.**

```bash
# Check for new files
git status --short | grep "^??"
```

**If there are new files, automatically execute:**

```bash
# Safely stage all new files (handles empty list and special filenames)
git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do git add -- "$f"; done
```

**Explanation:**

- `-z` uses null character to separate filenames, correctly handles filenames with spaces/newlines
- `while IFS= read -r -d ''` reads filenames one by one
- `git add -- "$f"` uses `--` separator, correctly handles filenames starting with `-`
- When no new files exist, loop body doesn't execute, safely skipped
- This won't stage modified files, only handles new files
- codex needs files to be tracked by git for proper review

### 3. Evaluate Task Difficulty and Invoke codex-runner

**Count change scale:**

```bash
# Get summary line for ALL changes (staged + unstaged)
# IMPORTANT: Must use 'HEAD' as base to include both staged and unstaged changes
git diff --stat HEAD | tail -1
```

**Why use `git diff --stat HEAD`:**
- `git diff --stat` only shows unstaged changes
- `git diff --cached --stat` only shows staged changes
- `git diff --stat HEAD` shows BOTH staged and unstaged changes combined
- The last line (`tail -1`) is the summary line with total file count and line changes

**Difficulty Assessment Criteria:**

**Model + Reasoning Effort Combinations:**

Only recommend `gpt-5.3-codex`; choose `model_reasoning_effort` and timeout based on task complexity.

| Combination | Quality | Time | Timeout | Recommended For |
|-------------|---------|------|---------|-----------------|
| `model=gpt-5.3-codex model_reasoning_effort=xhigh` | High | ~8-20 min | 15-40 min | Difficult tasks, critical code, architecture changes |
| `model=gpt-5.3-codex model_reasoning_effort=high` | Good | ~5-6 min | 10 min | Normal tasks (default) |

**Critical Tasks** (meets any condition, use highest reasoning effort):

- Modified files ≥ 30
- Total code changes (insertions + deletions) ≥ 2000 lines
- Involves core architecture/algorithm changes (user explicitly mentioned)
- Config: `--config model=gpt-5.3-codex --config model_reasoning_effort=xhigh`, timeout 40 minutes

**Difficult Tasks** (meets any condition):

- Modified files ≥ 10
- Total code changes (insertions + deletions) ≥ 500 lines
- Single metric: insertions ≥ 300 lines OR deletions ≥ 300 lines
- Cross-module refactoring
- Default config: `--config model=gpt-5.3-codex --config model_reasoning_effort=xhigh`, timeout 15 minutes

**Normal Tasks** (other cases):

- Default config: `--config model=gpt-5.3-codex --config model_reasoning_effort=high`, timeout 10 minutes

**Evaluation Method:**

You MUST parse the `git diff --stat HEAD` output correctly to determine difficulty:

```bash
# Get the summary line (last line of git diff --stat HEAD)
git diff --stat HEAD | tail -1
# Example outputs:
# "20 files changed, 342 insertions(+), 985 deletions(-)"
# "1 file changed, 50 insertions(+)"  # No deletions
# "3 files changed, 120 deletions(-)"  # No insertions
```

**Critical: Why the summary line matters:**
- Each file shows individual stats: `file.go | 171 ++++++++++++++++++++-`
- Only the LAST line has the total: `6 files changed, 1341 insertions(+), 18 deletions(-)`
- You must extract the last line with `tail -1` to get accurate totals

**Parsing Rules:**
1. Extract file count from "X file(s) changed" (handle both "1 file" and "N files")
2. Extract insertions from "Y insertion(s)(+)" if present (handle both "1 insertion" and "N insertions"), otherwise 0
3. Extract deletions from "Z deletion(s)(-)" if present (handle both "1 deletion" and "N deletions"), otherwise 0
4. Calculate total changes = insertions + deletions

**Important Edge Cases:**
- Single file: `"1 file changed"` (singular form)
- No insertions: Git omits `"insertions(+)"` entirely → treat as 0
- No deletions: Git omits `"deletions(-)"` entirely → treat as 0
- Pure rename: May show `"0 insertions(+), 0 deletions(-)"` or omit both

**Decision Logic (check in order, first match wins):**
- IF file_count >= 30 OR total_changes >= 2000 → **Critical** (gpt-5.3-codex + xhigh)
- IF file_count >= 10 → **Difficult** (gpt-5.3-codex + xhigh)
- IF total_changes >= 500 → **Difficult** (gpt-5.3-codex + xhigh)
- IF insertions >= 300 OR deletions >= 300 → **Difficult** (gpt-5.3-codex + xhigh)
- ELSE → **Normal** (gpt-5.3-codex + high)

**Example Cases:**
- ⭐ "50 files changed, 2000 insertions(+), 1500 deletions(-)" → **关键任务**，使用 `model=gpt-5.3-codex model_reasoning_effort=xhigh`，超时 40 分钟（核心架构变更）
- ✅ "20 files changed, 342 insertions(+), 985 deletions(-)" → **困难任务**，使用 `model=gpt-5.3-codex model_reasoning_effort=xhigh`，超时 15 分钟
- ✅ "5 files changed, 600 insertions(+), 50 deletions(-)" → **困难任务**，使用 `model=gpt-5.3-codex model_reasoning_effort=xhigh`，超时 15 分钟
- ❌ "3 files changed, 150 insertions(+), 80 deletions(-)" → **普通任务**，使用 `model=gpt-5.3-codex model_reasoning_effort=high`，超时 10 分钟
- ❌ "1 file changed, 50 insertions(+)" → **普通任务**，使用 `model=gpt-5.3-codex model_reasoning_effort=high`，超时 10 分钟

**Invoke codex-runner Subtask:**

Use Task tool to invoke codex-runner, passing complete command (including Lint + codex review):

```
Task parameters:
- subagent_type: Bash
- description: "Execute Lint and codex review"
- timeout: 2400000 (40 minutes for critical tasks) / 900000 (15 minutes for difficult tasks) / 600000 (10 minutes for normal tasks)
- prompt: Choose corresponding command based on project type and difficulty

Go project - Critical task:
  go fmt ./... && go vet ./... && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh
  (timeout: 2400000)

Go project - Difficult task:
  go fmt ./... && go vet ./... && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh
  (timeout: 900000)

Go project - Normal task:
  go fmt ./... && go vet ./... && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=high
  (timeout: 600000)

Node project - Critical task:
  npm run lint:fix && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh
  (timeout: 2400000)

Node project - Difficult task:
  npm run lint:fix && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh
  (timeout: 900000)

Node project - Normal task:
  npm run lint:fix && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=high
  (timeout: 600000)

Python project - Critical task:
  black . && ruff check --fix . && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh
  (timeout: 2400000)

Python project - Difficult task:
  black . && ruff check --fix . && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh
  (timeout: 900000)

Python project - Normal task:
  black . && ruff check --fix . && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=high
  (timeout: 600000)

Clean working directory:
  codex review --commit HEAD --config model=gpt-5.3-codex --config model_reasoning_effort=high
  (timeout: 600000)
```

### 4. Self-Correction and Severity-Driven Fixes

If Codex finds Changelog description inconsistent with code logic:

- **Code error** → Fix code
- **Description inaccurate** → Update Changelog

If Codex reports **P0 / P1 / P2** issues, you must **proactively fix them immediately** instead of stopping at reporting.

**Required behavior:**

1. **P0 / P1 / P2 present** → directly modify code or related files to fix the issue
2. **After fixing** → rerun the necessary lint / validation / review command to confirm the issue is resolved
3. **Only report completion after recheck** → clearly state what was fixed and what verification passed
4. **P3 or lower / suggestion only** → may report without automatic modification unless the user explicitly asks for further cleanup

**Fix priority:**
- **P0**: Blocker, security, data loss, correctness failure → must fix first
- **P1**: High-impact functional or logic bug → must fix
- **P2**: Important maintainability / correctness issue with clear fix → should proactively fix in the same run

**Constraints:**
- Keep fixes minimal and directly related to the reported issue
- Do not expand scope into unrelated refactors
- Preserve existing style and architecture unless the issue requires structural adjustment

## Complete Review Protocol

1. **[GATE] Check CHANGELOG** - Auto-generate and write if not updated (leverage current context to understand change intention)
2. **[PREPARE] Stage Untracked Files** - Add all new files to git staging area (avoid codex P1 error)
3. **[EXEC] Task → Lint + codex review** - Invoke Task tool to execute Lint and codex (isolated context, reduce waste)
4. **[FIX] Severity-Driven Self-Correction** - Fix code or update description when intention ≠ implementation; proactively fix P0/P1/P2 issues and rerun checks

## Codex Review Command Reference

### Basic Syntax

```bash
codex review [OPTIONS] [PROMPT]
```

**Note**: `[PROMPT]` parameter cannot be used with `--uncommitted`, `--base`, or `--commit`.

### Common Options

| Option                     | Description                                                      | Example                                                      |
| -------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ |
| `--uncommitted`            | Review all uncommitted changes in working directory (staged + unstaged + untracked) | `codex review --uncommitted`                                 |
| `--base <BRANCH>`          | Review changes relative to specified base branch                 | `codex review --base main`                                   |
| `--commit <SHA>`           | Review changes introduced by specified commit                    | `codex review --commit HEAD`                                 |
| `--title <TITLE>`          | Optional commit title, displayed in review summary               | `codex review --uncommitted --title "feat: add JSON parser"` |
| `-c, --config <key=value>` | Override configuration values                                    | `codex review --uncommitted -c model="gpt-5.3-codex"`      |

### Usage Examples

```bash
# 1. Review all uncommitted changes (most common)
codex review --uncommitted

# 2. Review latest commit
codex review --commit HEAD

# 3. Review specific commit
codex review --commit abc1234

# 4. Review all changes in current branch relative to main
codex review --base main

# 5. Review changes in current branch relative to develop
codex review --base develop

# 6. Review with title (title shown in review summary)
codex review --uncommitted --title "fix: resolve JSON parsing errors"

# 7. Review using the recommended model
codex review --uncommitted -c model="gpt-5.3-codex"
```

### Important Limitations

- `--uncommitted`, `--base`, `--commit` are mutually exclusive, cannot be used together
- `[PROMPT]` parameter is mutually exclusive with the above three options
- Must be executed in a git repository directory

## Important Notes

- Ensure execution in git repository directory
- **Timeout automatically adjusted based on task difficulty:**
  - Critical tasks: 40 minutes (`timeout: 2400000`)
  - Difficult tasks: 15 minutes (`timeout: 900000`)
  - Normal tasks: 10 minutes (`timeout: 600000`)
- codex command must be properly configured and logged in
- codex automatically processes in batches for large changes
- **CHANGELOG.md must be in uncommitted changes, otherwise Codex cannot see intention description**

## Design Rationale

**Why separate contexts?**

1. **CHANGELOG update needs current context**: Understanding user's previous conversation and task intention to generate accurate change description
2. **Codex review doesn't need conversation history**: Only needs code changes and CHANGELOG, more efficient to run independently
3. **Reduce token consumption**: codex review as independent subtask, doesn't carry irrelevant conversation context
