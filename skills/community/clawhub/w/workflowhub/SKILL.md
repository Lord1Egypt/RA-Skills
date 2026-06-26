---
name: work-style-memory
description: Use when the user wants OpenClaw or Codex to remember their way of working as reusable SOPs, workflows, queues, or "how I do things". Best for repeated multi-step tasks where the agent should proactively check saved workflows before starting, ask whether to reuse an existing SOP when there is a strong match, and ask whether to save or update a workflow after the task.
---

# Work Style Memory

## Overview

This skill treats the user's repeated ways of working as a local workflow library instead of burying them inside a one-off prompt. The workflow file is the source of truth; the agent uses it to match similar requests, generate an execution brief, and ask whether the run should be saved back into the library.

Use this skill when the user says things like:

- "Remember how I usually do this"
- "Can you turn this into an SOP or workflow"
- "Ask me whether to reuse my previous process"
- "Prefill the same tools, templates, or baseline parameters"
- "I need a local UI to edit my workflows"

Do not use this skill for truly one-off tasks or very small requests that do not benefit from storing a reusable process.

## Operating Model

The skill works in four phases:

1. Match the current request against saved workflows.
2. If there is a strong match, ask whether to use the existing workflow.
3. Compile the workflow into an execution brief and perform the task.
4. At the end, ask whether to save a new workflow or update the matched one.

The workflow library should be editable outside the skill. The recommended storage layout is:

- Project-specific workflows: `.openclaw/workflows/*.json`
- Personal cross-project workflows: `$CODEX_HOME/work-style-memory/workflows/*.json`

Prefer project-local workflows when the process is tied to a repository, team, or codebase. Prefer the global store when the process reflects the user's personal way of working across contexts.

When this skill is active during a normal chat task, the workflow check should happen as part of the agent's task handling flow, not only in the local UI.

## Matching Rules

When this skill is active, build a candidate list by comparing the current request with saved workflows using:

- keywords
- toolchain overlap
- recent actions in the current session

Behavior rules:

- Before doing a non-trivial task, proactively check the workflow library.
- If there is one high-confidence match, ask a short confirmation question before using it.
- If there are two plausible matches, present the top two briefly and ask which one to use.
- If confidence is low, continue normally and offer to save a workflow after the task.
- Never silently apply a workflow that can trigger writes, external calls, or other meaningful side effects unless the user already asked for it in this turn.
- Never auto-run a matched workflow just because it looks like the same task. Matching only gives permission to suggest reuse, not to execute.
- The only time a matched workflow may be used without an extra confirmation question is when the user explicitly says in the current turn that they want to use the previous SOP, workflow, or usual process.

## Running A Workflow

A workflow is not the final prompt. It is structured memory that gets compiled into a short execution brief.

When executing a matched workflow:

1. Load the workflow file.
2. Convert the workflow into an execution brief that includes:
   - goal
   - trigger keywords
   - ordered steps
   - preferred tools
3. Execute the task using that brief rather than pasting the raw JSON to the model.

Use [render_workflow_prompt.py](./scripts/render_workflow_prompt.py) to generate a deterministic draft brief when helpful.
Use [match_workflows.py](./scripts/match_workflows.py) when you want a deterministic similarity check against the saved workflow library.
Read [runtime-behavior.md](./references/runtime-behavior.md) for the expected preflight behavior during normal chat tasks.

## Capturing A New Workflow

After completing a task, ask whether to save it if any of these are true:

- the task required several non-trivial steps
- the user gave process-specific preferences
- the user corrected the order, tools, or keywords
- the process is likely to recur

When saving or updating a workflow, record:

- what kind of request it handles
- trigger keywords
- preferred tools and order of steps
- a short summary

Use [workflow-template.json](./assets/workflow-template.json) as the starting shape. Use [new_workflow.py](./scripts/new_workflow.py) to scaffold a file quickly.
Use [capture_workflow.py](./scripts/capture_workflow.py) when you want to turn a real task description into a draft workflow quickly.
Use [save_workflow.py](./scripts/save_workflow.py) when the user confirms that the task should be saved or used to update an existing workflow.

## Editing And UI Expectations

This skill assumes the workflow library is user-editable. The local UI should edit the same files that the skill reads.

The minimum useful UI has:

- a workflow list with search and recent keywords
- a detail page with name, summary, keywords, steps, and tool preferences
- an edit form for summary, keywords, steps, and toolchains
- a last updated indicator
- a diff-friendly view so the user can safely update an existing workflow

This skill bundle includes a runnable MVP UI at [ui/server.py](./ui/server.py), which serves a local editor for the workflow JSON files.
The local UI can also:

- suggest similar workflows from a real task description
- ask whether to reuse a likely SOP match
- generate a workflow draft from a real task and its observed steps
- render an execution brief from the currently selected workflow

See [local-ui-spec.md](./references/local-ui-spec.md) for the recommended interface model.

## Workflow File Shape

Use JSON for the initial implementation so the files are easy to render, diff, validate, and edit from scripts or a local UI. The schema and field guidance are in [workflow-schema.md](./references/workflow-schema.md).

Important conventions:

- Keep workflows short and composable; do not store huge transcripts.
- Store concise step descriptions, not chain-of-thought.
- Keep triggers to a small keyword list.
- Prefer simple workflows over exhaustive configuration.

## Example Interaction Pattern

When a similar request arrives:

1. Check the workflow library before starting the task.
2. Detect likely workflow match.
3. Ask: "I found your `pr-review` workflow for this. Do you want me to use that SOP?"
4. If yes, run using the compiled brief.
5. After the run, ask whether today's differences should update the workflow.

When no workflow matches:

1. Complete the task normally.
2. Summarize the process in a compact way.
3. Ask: "Want me to save this as a reusable workflow for next time?"

## Reference Files

- Read [workflow-schema.md](./references/workflow-schema.md) when creating or editing workflow files.
- Read [local-ui-spec.md](./references/local-ui-spec.md) when discussing or implementing the editable local UI.
- Read [runtime-behavior.md](./references/runtime-behavior.md) when the skill is being used during a normal chat task.
- Use [workflow-template.json](./assets/workflow-template.json) as the default starter asset.
