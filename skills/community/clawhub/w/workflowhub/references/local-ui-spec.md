# Local UI Spec

This reference describes the minimum useful local UI for the `work-style-memory` skill.

## Product Goal

Give the user a safe local place to inspect, edit, and evolve their workflows without editing prompts by hand.

The UI edits the same workflow files that the skill reads. Avoid a separate hidden database in the MVP.

This UI is only for workflow management and editing.
Runtime behaviors such as workflow matching, asking whether to reuse an SOP, and turning a real task into a workflow belong to the skill's chat-time behavior, not to this UI.

## MVP In This Skill Bundle

A runnable MVP is included at:

- `ui/server.py`
- `ui/static/index.html`
- `ui/static/app.js`
- `ui/static/styles.css`

Launch it with:

```bash
python3 /Users/zyq/Desktop/skills/work-style-memory/ui/server.py --dir ./.openclaw/workflows
```

Then open `http://127.0.0.1:8765`.

Do not copy `/path/to/...` literally as a directory. The `--dir` value must be a real writable path on your machine.

## Minimum Screens

### 1. Workflow List

The list page should support:

- search by name, summary, and keyword
- quick indicators for recent keywords and update time
- actions for create and edit

Suggested list columns:

- name
- summary
- keywords
- last updated

### 2. Workflow Detail

The detail page should show:

- summary
- keywords
- ordered steps
- tool preferences
- update time

### 3. Workflow Editor

The editor should use forms instead of raw JSON by default.

Important editor sections:

- basic info
- keywords
- step builder
- tool preferences

Useful UX rules:

- generate `id` automatically from `name`
- validate duplicate generated ids before saving
- generate step ids automatically from row order
- show JSON preview as a secondary tab, not the primary editing mode

## Event Flow

Recommended flow for a matched request:

1. Request arrives.
2. System finds one or more likely workflow matches.
3. User sees a prompt to reuse an existing workflow.
4. User confirms.
5. Execution brief is rendered.
6. Task runs.
7. Post-run review offers "save as new" or "update existing".

Recommended flow for a new pattern:

1. Request arrives.
2. No good match is found.
3. Task runs normally.
4. Post-run review suggests saving the process as a workflow.

## Data Design Notes

For the MVP:

- store workflows as plain JSON files
- optionally store run metadata in a separate lightweight file if needed
- avoid storing transcripts by default
- keep save/update actions diff-friendly

Suggested metadata file if needed later:

- `.openclaw/workflow-runs/index.json`

## Safety Rules

The UI should make these boundaries visible:

- whether a workflow can cause writes
- whether a workflow can trigger external calls
