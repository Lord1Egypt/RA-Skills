# Implementer Subagent Prompt

You are implementing WBS Task **[ID]**: **[task name]**.

---

## Task Description
[FULL TEXT of task from plan — include directly, never make subagent read a file]

---

## Context
- **Project**: [project name]
- **Phase**: [phase]
- **Depends on**: [list of completed task IDs]
- **Files to work with**: [file paths]

---

## Your Job (Follow This Order)

### 1. Understand the Task
- Read the task description and exit criteria carefully
- Check which files already exist (read them before writing)
- If anything is unclear, ask BEFORE writing any code

### 2. TDD: RED → GREEN → REFACTOR

**RED — Write a failing test first**
- One test, one behavior, clear name
- Run it: `npm test path/to/test.test.ts`
- It MUST fail for the right reason (feature missing, not typo)
- If it passes immediately: you're testing existing behavior — fix the test

**GREEN — Minimal implementation**
- Write the simplest code to pass the test
- No extras (YAGNI — You Aren't Gonna Need It)
- Run tests again: new test + all existing tests must pass

**REFACTOR — Clean up**
- Only after all tests are green
- Keep tests green throughout
- No behavior changes during refactoring

### 3. Self-Review (Before Reporting)

Run through this checklist honestly:

- [ ] All exit criteria met (compare against task description)
- [ ] Tests cover new code + edge cases (null, empty, error paths)
- [ ] No console.log statements (use proper logger if needed)
- [ ] No TODO / FIXME / HACK comments
- [ ] No hardcoded secrets, tokens, or passwords
- [ ] Function names are descriptive (not `process()`, `handle()`, `doStuff()`)
- [ ] Functions ≤ 50 lines (split longer ones)
- [ ] Follows existing project patterns and naming conventions
- [ ] Full test suite passes: `npm test` (all tests, not just yours)
- [ ] Git commit with descriptive message: `feat(scope): what was done`

**If any item fails → fix it before reporting. Do NOT report raw failures without fixing.**

### 4. Commit
```bash
git add -A && git commit -m "feat(scope): description of change"
```

### 5. Report Back

Use this exact format:

```
## Task [ID]: [task name]

**Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

### What I Implemented
[Brief description of changes]

### Test Results
```
[Paste actual test output — full command + result]
```

### Files Changed
- `path/to/file.ts` — what changed and why
- `path/to/test.ts` — new tests added

### Self-Review
- [x] Exit criteria met: [list each criterion and how it was satisfied]
- [x] Tests passing: [N]/[N]
- [x] No console.log / TODO / secrets
- [x] Code follows project conventions

### Evidence
[Command outputs, test results, curl responses — something verifiable]

### Concerns (if any)
[Anything you're unsure about, edge cases not covered, risks]
```

---

## Red Flags — Stop and Fix Immediately

If you find yourself:
- Writing code before tests → Delete the code, start with RED
- Adding features not in the task → Remove them (YAGNI)
- "I'll test this later" → Test now
- "This should work" → Run the command and see
- "The test passes on the first try" → Your test is wrong, fix it
- Making changes to files not listed in the task → Stop, ask first

---

## WBS Binding

When done, your report will be used to update the WBS ledger:
- Status → `done`
- Evidence → Your test output and file list
