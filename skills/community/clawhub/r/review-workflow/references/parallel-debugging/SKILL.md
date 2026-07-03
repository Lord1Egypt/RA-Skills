---
name: parallel-debugging
description: >
  Dual-mode skill for debugging and fix generation.
  Review Fix Mode: generates concrete diff fixes for issues found in code review (used by review-workflow Step 3).
  Bug Investigation Mode: debugs unknown bugs using competing hypotheses with parallel investigation, evidence collection, and root cause arbitration.
version: 1.1.0
allowed-tools: Bash, Read
---

# Parallel Debugging

Framework for debugging complex issues using the Analysis of Competing Hypotheses (ACH) methodology with parallel agent investigation.

## When to Use This Skill

- Bug has multiple plausible root causes
- Initial debugging attempts haven't identified the issue
- Issue spans multiple modules or components
- Need systematic root cause analysis with evidence
- Want to avoid confirmation bias in debugging

## Operation Modes

This skill operates in two modes, auto-detected from the caller's input:

| Mode | Trigger | Input | Task |
|------|---------|-------|------|
| **Review Fix Mode** | Called by `review-workflow` Step 3 | `[REVIEW_REPORT]` — already-identified issues | Generate concrete diff fixes for each issue |
| **Bug Investigation Mode** | Standalone debugging of unknown bugs | Symptoms, error logs, reproduction steps | Generate hypotheses, collect evidence, determine root cause |

When input is a structured review report containing issues tagged with `#I`/`#C`/`#S` identifiers, operate in **Review Fix Mode**. Otherwise, operate in **Bug Investigation Mode**.

---

## Review Fix Mode (review-workflow Step 3)

When invoked by `review-workflow`, the input is a `[REVIEW_REPORT]` containing already-identified issues. The task is to generate concrete fixes — NOT to hypothesize about unknown root causes.

### Input

`[REVIEW_REPORT]` — structured report containing:
- Intent-layer issues (`#I01`, `#I02`, ...)
- Specification-layer issues (`#C01`, `#C02`, ...)
- Suggestions (`#S01`, `#S02`, ...)

### Processing Per Issue

For each issue in the review report:

1. **Analyze why it happened** — design oversight, missing edge case, incorrect assumption, copy-paste error, etc.
2. **Design a minimal fix** — target the root cause, not the symptom; prefer surgical changes
3. **Verify fix against review rules** — ensure the fix doesn't introduce new violations of function-length limits, naming rules, TODO/FIXME rules, or loop-performance rules

### Output Format (Per Issue)

```
#### 问题 [#I01 / #C01 / #S01]：<问题简述>

**严重程度**：🔴 blocking / 🟡 important / 🟢 nit / 💡 suggestion

**根因分析**
<为什么会出现这个问题，源头在哪里>

**修复方案（diff 形式）**
--- a/path/to/file
+++ b/path/to/file
@@ ... @@
- 原有代码
+ 修复代码

**影响范围**
- 直接修改文件：<列表>
- 间接影响文件：<列表>
- 风险评估：低 / 中 / 高

**测试建议**
- <用例名>（正向 / 边界 / 异常）
```

### Output Bundle

After processing all issues, bundle all fixes into `[PATCH_LIST]` — an ordered list of all fixes with their metadata, sorted by severity (blocking first).

### Quality Gate

Before returning `[PATCH_LIST]` to `review-workflow`, verify:
- [ ] Each fix addresses the exact issue in `[REVIEW_REPORT]`
- [ ] No fix introduces new function-length violations (>150 lines blocking, >80 lines warning)
- [ ] No fix introduces new `TODO`/`FIXME` without an accompanying issue reference
- [ ] No fix adds a loop containing DB queries or network calls
- [ ] All fixes maintain or improve naming clarity (no single-letter variables except loop indices)

---

## Bug Investigation Mode

## Hypothesis Generation Framework

Generate hypotheses across 6 failure mode categories:

### 1. Logic Error

- Incorrect conditional logic (wrong operator, missing case)
- Off-by-one errors in loops or array access
- Missing edge case handling
- Incorrect algorithm implementation

### 2. Data Issue

- Invalid or unexpected input data
- Type mismatch or coercion error
- Null/undefined/None where value expected
- Encoding or serialization problem
- Data truncation or overflow

### 3. State Problem

- Race condition between concurrent operations
- Stale cache returning outdated data
- Incorrect initialization or default values
- Unintended mutation of shared state
- State machine transition error

### 4. Integration Failure

- API contract violation (request/response mismatch)
- Version incompatibility between components
- Configuration mismatch between environments
- Missing or incorrect environment variables
- Network timeout or connection failure

### 5. Resource Issue

- Memory leak causing gradual degradation
- Connection pool exhaustion
- File descriptor or handle leak
- Disk space or quota exceeded
- CPU saturation from inefficient processing

### 6. Environment

- Missing runtime dependency
- Wrong library or framework version
- Platform-specific behavior difference
- Permission or access control issue
- Timezone or locale-related behavior

## Evidence Collection Standards

### What Constitutes Evidence

| Evidence Type     | Strength | Example                                                         |
| ----------------- | -------- | --------------------------------------------------------------- |
| **Direct**        | Strong   | Code at `file.ts:42` shows `if (x > 0)` should be `if (x >= 0)` |
| **Correlational** | Medium   | Error rate increased after commit `abc123`                      |
| **Testimonial**   | Weak     | "It works on my machine"                                        |
| **Absence**       | Variable | No null check found in the code path                            |

### Citation Format

Always cite evidence with file:line references:

```
**Evidence**: The validation function at `src/validators/user.ts:87`
does not check for empty strings, only null/undefined. This allows
empty email addresses to pass validation.
```

### Confidence Levels

| Level               | Criteria                                                                            |
| ------------------- | ----------------------------------------------------------------------------------- |
| **High (>80%)**     | Multiple direct evidence pieces, clear causal chain, no contradicting evidence      |
| **Medium (50-80%)** | Some direct evidence, plausible causal chain, minor ambiguities                     |
| **Low (<50%)**      | Mostly correlational evidence, incomplete causal chain, some contradicting evidence |

## Result Arbitration Protocol

After all investigators report:

### Step 1: Categorize Results

- **Confirmed**: High confidence, strong evidence, clear causal chain
- **Plausible**: Medium confidence, some evidence, reasonable causal chain
- **Falsified**: Evidence contradicts the hypothesis
- **Inconclusive**: Insufficient evidence to confirm or falsify

### Step 2: Compare Confirmed Hypotheses

If multiple hypotheses are confirmed, rank by:

1. Confidence level
2. Number of supporting evidence pieces
3. Strength of causal chain
4. Absence of contradicting evidence

### Step 3: Determine Root Cause

- If one hypothesis clearly dominates: declare as root cause
- If multiple hypotheses are equally likely: may be compound issue (multiple contributing causes)
- If no hypotheses confirmed: generate new hypotheses based on evidence gathered

### Step 4: Validate Fix

Before declaring the bug fixed:

- [ ] Fix addresses the identified root cause
- [ ] Fix doesn't introduce new issues
- [ ] Original reproduction case no longer fails
- [ ] Related edge cases are covered
- [ ] Relevant tests are added or updated
