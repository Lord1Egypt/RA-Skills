# Runtime Behavior

Use this reference when the skill is active during a normal chat task.

## Goal

Make the agent proactively check the user's saved workflows during conversation, not only inside the local UI.

## Preflight Behavior

Before doing a non-trivial task:

1. Identify the likely workflow directory.
2. Run `scripts/match_workflows.py` against the current task description.
3. If the top match is high-confidence, ask whether to reuse that workflow before continuing.
4. If the user says yes, load that workflow and use `scripts/render_workflow_prompt.py` to produce a compact execution brief.

This confirmation is mandatory unless the user explicitly asked in the current turn to use the previous SOP, workflow, or usual process.

Recommended workflow directory order:

1. `./.openclaw/workflows`
2. `$CODEX_HOME/work-style-memory/workflows`

## Suggested User-Facing Prompt

If there is a high-confidence match, ask something short like:

`This looks similar to your "PR Review" workflow. Want me to reuse that SOP?`

If there are two plausible matches, offer the top two briefly and ask which one to use.

Do not skip this question just because the task is an obvious repeat. The workflow match is a suggestion, not automatic execution permission.

## Post-Run Capture Behavior

After finishing a task, offer to save or update a workflow when:

- the task had multiple meaningful steps
- the user corrected the order or preferred tools
- the process is likely to repeat

When the user agrees:

1. Summarize the task in one sentence.
2. Summarize the actual steps.
3. Run `scripts/capture_workflow.py` to create a draft, or `scripts/save_workflow.py` to write it directly.
4. If the run is clearly an update to an existing workflow, use `scripts/save_workflow.py --update <id>`.

## Interaction Boundary

The agent should not silently save a workflow without asking.

The intended pattern is:

1. preflight match
2. ask whether to reuse
3. execute
4. ask whether to save or update
