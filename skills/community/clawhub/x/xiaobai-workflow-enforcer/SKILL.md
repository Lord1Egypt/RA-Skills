---
name: xiaobai-workflow-enforcer
version: 1.0.0
description: Xiaobai Workflow Enforcer - Mandatory workflows for AI Agents. Design before code. Test before implement. Verify before claim. Inspired by Superpowers (161K stars).
emoji: 🔒
tags: [workflow, enforcement, tdd, quality, reliability, ai-agent]
---

# Xiaobai Workflow Enforcer 🔒

Mandatory workflows for AI Agents. Not suggestions, not "when appropriate" — **mandatory**.

Inspired by Superpowers (161K stars) which proved that enforced workflows transform chaotic AI outputs into reliable engineering.

## Core Philosophy

| Superpowers Principle | Xiaobai Implementation |
|----------------------|------------------------|
| Test-Driven Development | EVR + TDD skill |
| Systematic over ad-hoc | Workflow Checkpoint |
| Complexity reduction | Simplicity Check |
| Evidence over claims | Verification Gate |

## Mandatory Workflows

### Workflow 1: Pre-Action Design Gate 🔒

**Trigger:** Before any multi-step task or code creation

**Mandatory Steps:**
1. STOP. Don't write code yet.
2. Ask clarifying questions (minimum 3)
3. Present design/spec in chunks
4. Get user sign-off on design
5. Save design document

```
❌ Wrong:
User: Build me a scraper
Agent: [Writes code]

✅ Right:
User: Build me a scraper
Agent: Before I code, let me understand:
       1. What site are we scraping?
       2. What data do you need?
       3. How often should it run?
       4. Any rate limits to consider?
       [After answers, presents design]
       Does this design match what you need?
```

### Workflow 2: Implementation Planning 🔒

**Trigger:** After design approval, before implementation

**Mandatory Steps:**
1. Break into 2-5 minute tasks
2. Each task has: file path, exact code, verification step
3. Present plan for approval
4. Save plan to checkpoint file

```
Plan Format:

## Task 1: Create scraper module (3 min)
- File: src/scraper.py
- Code: [exact code or pseudocode]
- Verify: `python -c "import scraper"`

## Task 2: Add rate limiting (2 min)
- File: src/scraper.py
- Code: [exact changes]
- Verify: Run with test request, check delay

...
```

### Workflow 3: Test-First Gate 🔒

**Trigger:** Before implementing any function

**Mandatory Steps:**
1. Write test first
2. Run test, confirm it FAILS (RED)
3. Write minimal code to pass
4. Run test, confirm it PASSES (GREEN)
5. Refactor if needed
6. Commit only after GREEN

```
❌ Wrong:
[Writes function]
[Tests it manually]
"It works"

✅ Right:
1. Write test_function()
2. Run: pytest test_module.py
3. See: FAILED (expected)
4. Write function()
5. Run: pytest test_module.py
6. See: PASSED
7. Commit
```

### Workflow 4: Execution Gate 🔒

**Trigger:** During task execution

**Mandatory Steps:**
1. Read task from plan
2. Execute exactly as planned
3. Verify (run command, check output)
4. Update checkpoint
5. Only then move to next task

```
Checkpoint Update:
- Task 1: DONE (verified: scraper.py imports successfully)
- Task 2: IN_PROGRESS
- Tasks 3-5: PENDING
```

### Workflow 5: Verification Gate 🔒

**Trigger:** Before claiming "done" or "complete"

**Mandatory Steps:**
1. Run verification command
2. Show output to user
3. Confirm evidence matches claim
4. Only then say "done"

```
❌ Wrong:
"Scraper is done!"

✅ Right:
"Scraper implementation complete.

Verification:
- Module imports: ✅
- Test suite passes: ✅ (5/5)
- Sample scrape works: ✅

Evidence:
[Output from test run]

Would you like me to proceed with deployment?"
```

## Workflow Enforcement Protocol

### Before Any Action

```
1. Is this a multi-step task?
   → Yes → Trigger Workflow 1 (Design Gate)

2. Is there a plan?
   → No → Trigger Workflow 2 (Planning)

3. Does this involve code?
   → Yes → Trigger Workflow 3 (Test-First)

4. Is task in progress?
   → Yes → Trigger Workflow 4 (Execution Gate)

5. About to say "done"?
   → Yes → Trigger Workflow 5 (Verification Gate)
```

### Blockers That Must Stop Progress

| Condition | Action |
|-----------|--------|
| No design doc | Don't code, ask questions first |
| No plan | Don't execute, create plan first |
| No test | Don't write function, write test first |
| Test failing | Don't continue, fix the code |
| No verification | Don't say "done", verify first |

## Integration with Other Xiaobai Skills

- **EVR Framework** — Verification gate implementation
- **Workflow Checkpoint** — Plan and progress tracking
- **Skill Quality Eval** — Measure workflow compliance
- **Self-Improve** — Learn from workflow violations

## Anti-Patterns (What This Skill Prevents)

| Anti-Pattern | Why It's Bad | Workflow Fix |
|--------------|--------------|--------------|
| Jumping to code | Solves wrong problem | Design Gate |
| No plan | Chaotic execution | Planning Gate |
| Write-then-test | Tests that pass trivially | Test-First Gate |
| Skipping verification | Silent failures | Verification Gate |
| Claiming done prematurely | User finds out later | Execution Gate |

## Quick Reference Card

```
Before Coding:    DESIGN → APPROVE → PLAN → APPROVE
While Coding:     TEST(RED) → CODE → TEST(GREEN) → REFACTOR
After Coding:     VERIFY → EVIDENCE → REPORT
Always:           CHECKPOINT after each step
```

## License

MIT
