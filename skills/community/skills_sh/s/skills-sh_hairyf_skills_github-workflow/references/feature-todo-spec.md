---
name: feature-todo-spec
description: Specification for the TODO.md file and task delegation process.
---

# TODO.md & Delegation

Defines the standard for defining work via `TODO.md` and delegating it to SubAgents.

## TODO.md Template

Create this file at the project root:

```markdown
# Task: <task title>

**Task link**: <link_or_desc>
**Status**: <status>
**Project**: <project_name>

## Problem description
<detailed_description_and_comments>

## Todo
- [ ] Analyze root cause
- [ ] Locate relevant code files
- [ ] Plan fix
- [ ] Implement fix
- [ ] Run checks (typecheck/test/lint)
- [ ] Complete (main agent will then commit and remove this file)

## Related files
<fill_after_analysis>

## Approach
1. Search for relevant keywords
2. Check API calls and type definitions
3. Inspect related components
4. Understand data flow
```

## Delegation Workflow

1. **Create**: Generate `TODO.md` with task details.
2. **Delegate**: Instruct a **SubAgent** to "Follow the instructions in `TODO.md`".
   - The SubAgent should: Analyze, Plan, Implement, Verify.
3. **Completion**:
   - Wait for SubAgent to finish or user to confirm "fix done".
   - **User Confirmation**: Explicitly ask "Fix is done. Confirm to commit and create PR?".
   - **Cleanup**: Delete `TODO.md`.
   - **Commit**: Stage files and commit with a message derived from the task title.

## Key Points
- `TODO.md` acts as the contract for the SubAgent.
- **NEVER** commit `TODO.md`.
- Always require user confirmation before the final commit.
