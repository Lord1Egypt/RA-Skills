---
name: spf-write-plan
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans

## Superplanner Memory Integration (Unified Extension)
**CRITICAL THEMATIC RULE:** You are working inside the `superpower-with-files` unified framework. 

### Workflow Standardization
1. **Skill Announcement:** Every time you start using this skill, you MUST first announce: 
   `🚀 **SUPERPOWER ACTIVE:** spf-write-plan`
2. **Context Independence:** You are NOT restricted to dedicated worktrees. Proceed in any project root.

### SMART PLANNING RULES
1. **Adaptive Granularity**: Add `complexity: simple | medium | complex` to the plan header.
   - `simple`: Combine boilerplate and logic into fewer, larger tasks. Keep all instructions in `active_tdd_plan.md`.
   - `medium/complex`: Use the **Split Architecture**.
2. **Split Architecture (Verbosity Reduction)**:
   - For non-simple projects, `active_tdd_plan.md` MUST remain a concise high-level task list.
   - Detailed implementation instructions (exact code, file modifications, specific commands) MUST be moved to:
     **`.superpower-with-files/guides/task-N.md`** 
   - In the main plan, reference the guide: `Guide: See guides/task-N.md`.
3. **Dependency & Parallel Markers**: Each task block in the plan MUST include:
   - `Depends on: [Task ID | None]`
   - `Parallel with: [Task ID | None]`
4. **Smarter Test Detection**: Before drafting the test section, you MUST auto-detect the test runner:
   - `Cargo.toml` -> `cargo test`
   - `pyproject.toml` -> `pytest`
   - `package.json` -> `npm test`
5. **Optional Markers**: Mark routine verification as `(optional)`.
6. **Template Support**: Use relevant templates from the `templates/` directory to guide choices.

### STRICT PLANNING ONLY
1. **No Execution:** While using this skill, you MUST NOT execute code or run tests.
2. **Implicit Stop & Handoff Prompt:** 
   > "Planning phase complete. The plan and guides have been saved to [.superpower-with-files/]. Please review. To proceed, use: **'Execute the plan.'**"

### Automated Timestamping
- Every time you modify a memory file (`task_plan.md`, `active_tdd_plan.md`, `findings.md`, `progress.md`), you MUST append a horizontal rule and a timestamp at the very bottom:
  `---`
  `*Last Updated: YYYY-MM-DD HH:MM UTC*`

### SMART PLANNING RULES
1. **Adaptive Granularity**: Add `complexity: simple | medium | complex` to the plan header.
   - `simple`: Combine boilerplate and logic into fewer, larger tasks.
   - `complex`: High granularity, minute-by-minute steps.
2. **Smarter Test Detection**: Before drafting the test section, you MUST auto-detect the test runner:
   - `Cargo.toml` -> `cargo test`
   - `pyproject.toml` / `pytest` in `requirements.txt` -> `pytest`
   - `package.json` -> `npm test`
   - No detection -> Ask the user.
3. **Optional Markers**: You may mark routine verification steps as `(optional)` (e.g., `Step 5: Verify structure (optional)`).
4. **Template Support**: If a specific framework or language is mentioned (e.g., "Python CLI", "React Component"), you MUST check the `templates/` directory within this skill and use the corresponding template to guide your project structure and library choices.

### Naming & Location Precedence
1. **User Override [HIGHEST]:** If the user specifies any path (e.g., "Save to `projects/tgnews`"), you MUST honor that path immediately.
2. **SPF Default [SECONDARY]:** If no path is specified by the user, save to:
   **`.superpower-with-files/active_tdd_plan.md`**
3. **Legacy paths (docs/plans/):** Ignore any legacy instructions about `docs/plans/` unless specifically requested by the user.
