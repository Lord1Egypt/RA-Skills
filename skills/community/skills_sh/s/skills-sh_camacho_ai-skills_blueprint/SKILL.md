---
name: blueprint
description: Write the canonical ai-env blueprint plan for a multi-step task (Step 3 of /task). Runs one brainstorming round, uses ai-workspace/plans/TEMPLATE.md, and writes ai-workspace/plans/<name>.md. Skipped for one-sentence scope. Does NOT review — that is /review (Step 4).
---

# /blueprint

Write the canonical ai-env blueprint (plan file) for the current task. Requires /orient to have run first.

## Sequence

1. **Check prerequisites.** Confirm a worktree exists and /orient has identified the task. If not, stop and tell the user.
2. **Brainstorm (one round).** Invoke `/brainstorming` with the task description. One round only — capture direction, do not iterate.
3. **Read the template.** Read `ai-workspace/plans/TEMPLATE.md` from the repo root.
4. **Write the plan.** Create `ai-workspace/plans/<branch-slug>.md` with ALL template fields. For complex plans, read `references/planning-quality.md` and apply its checklist without copying the whole reference into the plan.

| Field | How to fill |
|---|---|
| **Branch** | Current branch name |
| **Target** | Branch to merge into. Default: detected via reflog parent (see below), falling back to `main`. Override only when intentionally retargeting. `/ship` reads this field. |
| **Created** | Today's date (YYYY-MM-DD) |
| **Status** | `In Progress` |
| **Threat model** | See selection table below |
| **Scope ceiling** | Keep template defaults (400/6 soft, 800/10 hard) |
| **Task** | 1-3 sentences: what and why |
| **Steps** | Checkbox list of concrete implementation steps |
| **Confidence Scaffold** | Required for `adversarial`. Recommended for complex `advisory`. |
| **Outcomes & Learnings** | Leave empty — populated by /archive |

5. **Commit the plan.** Stage and commit the plan file before handing off to `/review`:

   ```bash
   git -C "$WORKTREE" add ai-workspace/plans/<name>.md
   git -C "$WORKTREE" commit -m "blueprint: <name>"
   ```

   Required because `/review` works against committed state. A session crash or `/clear` after writing the plan but before `/review` runs loses the brainstorming work otherwise. See ADR-008 (`refs/wip/checkpoints/<branch>` Stop-hook backstop) for the recovery path if this step is skipped.

### Detecting the Target

The default Target is the branch this branch was cut from, read from the reflog:

```bash
TARGET=$(
  git reflog show HEAD --pretty=format:'%gs' \
    | grep "^branch: Created from" \
    | head -1 \
    | sed 's/branch: Created from //' \
    | sed 's|^origin/||'
)
TARGET=${TARGET:-main}
```

Falls back to `main` when the reflog is empty (web sessions, detached-HEAD creation). Use this whenever the user hasn't explicitly named a Target. Pure git — works in any environment without tool installs.

## Threat model selection

| Signal | Model |
|---|---|
| Internal tooling, refactor, docs, tests, config | `advisory` |
| Auth, secrets, input validation, CI, hooks, permissions | `adversarial` |
| Unsure | `adversarial` |

## Guardrails

- Do NOT review the blueprint. That is /review (Step 4).
- Do NOT start implementation. The blueprint is the deliverable.
- Do NOT skip any template field.
- Do NOT proceed to `/review` without committing the blueprint file first.
- If brainstorming reveals the task is one-sentence scope, say so and skip.
- Scope ceiling values are fixed — do not change them.
- Steps must be concrete actions with checkboxes, not vague phases.
- Include test steps explicitly. When tests need a separate author (TDD contract), list them as distinct tasks from implementation so /build dispatches test-writer and implementer separately.
- Do NOT invoke another planning skill; this skill owns ai-env plan writing.

## Output

After writing, report:

```
Plan written: ai-workspace/plans/<name>.md
Threat model: advisory|adversarial
Steps: <count>
Next step: /review (Step 4)
```
