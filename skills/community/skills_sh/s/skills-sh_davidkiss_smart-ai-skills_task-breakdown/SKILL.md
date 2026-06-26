---
name: task-breakdown
description: Use when you have specs or requirements for a multi-step task to break it down into detailed tasks, before executing it
---

# Writing Task Breakdown

## Overview

Write comprehensive task breakdowns assuming the expert who is going to implement the specs has zero context for our project and questionable taste. Document everything they need to know: which existing files to check, which files to touch for each task and what changes to make to them. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD.

Assume they are a skilled worker, but know almost nothing about our toolset or problem domain. Assume they don't know how to verify they are doing the right thing.

Analyze available agent skills and use all relevant ones to create the task breakdown.

**Announce at start:** "I'm using the task-breakdown skill to create a plan."

**Constraints:**
- Each task should have a last step that verifies the task was completed correctly
- The very last task should verify that after completing all tasks, the changes and actions were applied correctly and as intended by the specs, if provided

**Leverage existing skills**
- Identify relevant agent skills - other than this one and the @subagent-task-execution skill
- Output: "I'll use the following skills to help you with the task breakdown: @skill1, @skill2, ..."
- Load and use the identified skills to create the task breakdown

**Presenting the tasks:**
- Once you believe you have the full task breakdown, use a subagent to critique the task breakdown for self-correction - subagent must ground critique using websearch tool
- Then present the tasks one-by-one to the user
- Present tasks based on their dependencies on each other - e.g. if task B depends on task A, task A must be presented before task B
- Ask after each task whether it looks right so far
- Be ready to go back and clarify if something doesn't make sense - consider updating previous tasks based on user feedback, if needed
- When user confirms a task looks good, update `docs/YYYY-MM-DD-<feature-name>-tasks.md` with that task

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step

## Task Breakdown Document Header

**Every task breakdown MUST start with this header:**

```markdown
# [Task Name] Task Breakdown

**Goal:** [One sentence describing what this achieves]

**Approach:** [2-3 sentences about approach]

**Skills:** [List of skills to use]

**Tech Details:** [Key tools, services, technologies/libraries to use]

---
```

## Task Structure

```markdown
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


**Step 4: Cleanup code changes**
Use skill(s) if available to cleanup code changes

**Step 5: Review code changes**
Use skill(s) if available to review code changes.
Make sure code follows the project's coding standards and aligns with the specs and the task breakdown.

**Step 6: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS
```

## Remember
- Exact file paths always
- For coding tasks, complete code in task breakdown (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD

## Execution Handoff

After saving the task breakdown, offer task execution:

**"Task breakdown complete and saved to `docs/YYYY-MM-DD-<feature-name>-tasks.md`.**

**Subagent-based task execution (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

- **REQUIRED SUB-SKILL:** Use subagent-task-execution
- Stay in this session
- Fresh subagent per task + code review