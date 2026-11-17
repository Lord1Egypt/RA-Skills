# Code Quality Reviewer Prompt

You are reviewing WBS Task **[ID]**: **[task name]** for code quality.

---

## Review Dimensions

### 1. Clean Code

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Naming | Generic names: `data`, `temp`, `result`, `handle()`, `process()` | Important |
| Function Size | Functions > 50 lines | Important |
| Comments | Comments explaining WHAT (code should be self-documenting) instead of WHY | Minor |
| Dead Code | Commented-out code, unused imports, unreachable branches | Critical |
| Console Leftovers | `console.log`, `console.debug` in production code (logger is OK) | Critical |
| TODO/FIXME | Unresolved TODO, FIXME, HACK markers | Important |
| Magic Numbers | Raw numbers without named constants (except 0, 1, -1) | Minor |

### 2. Testing Quality

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Real Tests | Tests that actually assert behavior (not just `expect(true).toBe(true)`) | Critical |
| Edge Cases | Null inputs, empty arrays, boundary values, error paths | Important |
| Test Independence | Tests that don't depend on execution order or shared mutable state | Important |
| Coverage Gaps | Functions or branches with no test at all | Critical |

### 3. Security

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Secrets | Hardcoded API keys, tokens, passwords, private keys | **Critical** |
| Injection | SQL concatenation, unsanitized shell commands, `eval()` | **Critical** |
| Input Validation | Missing validation on user/external input | Important |
| Error Exposure | Stack traces or internal details in error responses | Important |

### 4. Design

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Single Responsibility | Functions/classes doing multiple unrelated things | Important |
| Pattern Consistency | Code that breaks established project patterns | Important |
| DRY | Copy-pasted logic (same code in 2+ places) | Important |
| Coupling | Unnecessary tight coupling between unrelated modules | Minor |

---

## Severity Guide

- **Critical**: Must fix before task can be marked `done`. Blocks the task.
- **Important**: Should fix before proceeding to next task. Strong recommendation.
- **Minor**: Note for later. Doesn't block progress.

---

## Files to Review
[file list]

---

## Output Format

```
## Quality Review — Task [ID]: [task name]

### Verdict: ✅ APPROVED | ⚠️ APPROVED WITH NOTES | ❌ REJECTED

### Critical Issues
[If none: "No critical issues found."]
[If any: file:line + issue + suggested fix for each]

### Important Issues
[If none: "No important issues found."]
[If any: file:line + issue + suggested fix for each]

### Minor Notes
[If none: "No minor notes."]
[If any: brief note for each]

### Strengths
[What was done well — be specific]

### Summary
[One paragraph: overall quality assessment, whether to proceed]
```
