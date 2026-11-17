---
version: "0.1.0"
required:
  - spec_content
  - spec_name
optional:
  - completed_tasks
---

Act as a senior software architect focused on incremental specification
evolution. Your task is to redesign the development steps for a
specification that has been modified.

Analyze the updated specification below, consider any already-completed
work, and produce a new set of implementation steps that will bring the
codebase in line with the revised requirements.

## Specification

The following is the updated specification. All new development steps
must fully satisfy its requirements.

<updated-specification>
{{ spec_content }}
</updated-specification>

{% if completed_tasks -%}
## Completed Steps

The following steps have already been implemented and committed.
Do NOT regenerate or duplicate them. Use them to:

- Determine the next available step ID for numbering.
- Understand what has already been built (avoid redundant work).
- Identify conflicts — if a completed step contradicts the updated
  specification, add a corrective step to fix it.

<completed-steps>
{{ completed_tasks }}
</completed-steps>

{% endif -%}

## Planning Principles

1. **No completed steps**: Do NOT include steps that are already done.
2. **Corrective steps**: If completed steps have implementation errors
   or conflict with the updated specification, add corrective steps
   to fix the divergence.
3. **Small batches**: Each step delivers a minimal, working increment
   that can be independently committed and verified.
4. **Self-contained**: Group production code and its tests in the same
   step — never split them into separate steps.
5. **Ordered by dependency**: List steps so that each builds on the
   previous one; no forward references.
6. **Sequential IDs**: Number steps starting from the next available ID
   after the last completed step (e.g., if step-2 is completed, start
   from `step-3`).

## Instructions

Using the updated specification and completed steps above, design the remaining
implementation steps and add them using `spex todo-helper`.

Before appending steps, run `show` to see the current state of the
todo list. After adding all steps, run `show` again to verify the
final plan is coherent and complete.

### Using spex todo-helper

**Append** a new step — use `--details-from-stdin` with a heredoc for
multi-line Markdown details:

```bash
$spex_skill_dir/scripts/spex todo-helper --name {{ spec_name }} append \
  --id step-N --step-name "Short name" --details-from-stdin <<'DETAILS'
Markdown-formatted description of what this step does,
including file changes, logic, and acceptance criteria.

- Use lists, bold, and inline code
- Do not use headings (`#`, `##`, etc.)
DETAILS
```

**Show** current steps (to review before adding more):

```bash
$spex_skill_dir/scripts/spex todo-helper --name {{ spec_name }} show \
  --format markdown
```

**Edit** a step (only specified fields are updated):

```bash
$spex_skill_dir/scripts/spex todo-helper --name {{ spec_name }} edit \
  --id step-N --step-name "Updated name" --details-from-stdin <<'DETAILS'
Updated multi-line details for this step.

- Revised implementation approach
- Added error handling requirements
DETAILS
```

**Remove** a step:

```bash
$spex_skill_dir/scripts/spex todo-helper --name {{ spec_name }} remove \
  --id step-N
```
