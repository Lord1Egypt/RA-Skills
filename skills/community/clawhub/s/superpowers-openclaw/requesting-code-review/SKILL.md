---
name: superpowers-open-requesting-code-review
description: >
  Use when completing tasks, implementing major features, or before merging to verify work meets requirements. Provides a self-review checklist since subagent-based review is not available on OpenClaw.
metadata:
  openclaw:
    emoji: "🔍"
---

# Requesting Code Review

Self-review your work to catch issues before they reach a human reviewer.

**Core principle:** Review early, review often. Since subagent-based review is not available on OpenClaw, use this structured self-review checklist.

## When to Review

**Mandatory:**
- After each task in plan execution
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## Self-Review Checklist

Run this checklist against your changes. Be honest — you're looking for real issues, not validation.

### 1. Spec Compliance

```
- [ ] Every requirement in the spec/plan has been implemented
- [ ] Nothing extra was added beyond the spec (YAGNI)
- [ ] All specified edge cases are handled
- [ ] No spec requirements were skipped or deferred
```

### 2. Code Quality

```
- [ ] Code is minimal — no over-engineering or premature abstraction
- [ ] Names are clear and describe what things do
- [ ] No magic numbers — constants are named
- [ ] No dead code or commented-out blocks
- [ ] Error handling is present where needed (and absent where not)
- [ ] No "TODO" or "FIXME" without a tracking issue
```

### 3. Testing

```
- [ ] Every new function/method has a test
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases are covered (empty input, null, boundary values)
- [ ] Error paths are tested
- [ ] All tests pass with clean output
- [ ] **REQUIRED: superpowers-open:test-driven-development** was followed
```

### 4. Safety

```
- [ ] No credentials, tokens, or secrets in code
- [ ] User input is validated at boundaries
- [ ] No unsafe shell command construction
- [ ] Dependencies are appropriate and necessary
```

### 5. Git Hygiene

```
- [ ] Changes are focused — one concern per commit
- [ ] Commit messages describe WHY, not WHAT
- [ ] No unrelated files accidentally included
- [ ] Branch is up to date with base
```

## What To Do With Findings

| Severity | Action |
|----------|--------|
| **Spec gap** (missing requirement) | Implement before proceeding |
| **Bug** (incorrect behavior) | Fix with TDD cycle |
| **Quality issue** (naming, magic number) | Fix now, one commit |
| **Minor** (style nit) | Note, fix if touching file anyway |

## If You Find Nothing

If the checklist is clean:
- **REQUIRED: Use superpowers-open:verification-before-completion** — run actual verification commands
- Only then proceed to **superpowers-open:finishing-a-development-branch** or the next task

## Common Mistakes

**Skipping review because "it's simple"**
- Simple code has simple bugs. Review it.

**Rubber-stamping your own work**
- You'll naturally overlook your own mistakes. Be skeptical.

**Fixing spec gaps silently**
- If you find a gap, tell your human partner. Don't just fill it in.

## Red Flags

**Never:**
- Skip review because "it's simple"
- Proceed with known issues unfixed
- Add "quick improvements" during review

**Always:**
- Complete the full checklist
- Fix spec gaps before proceeding
- Verify with real commands (not assumptions)
