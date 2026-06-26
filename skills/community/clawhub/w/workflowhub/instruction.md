# Work Style Memory

## Overview

`work-style-memory` is a workflow memory skill for repeated multi-step tasks.

It helps an agent:

- match a new task against saved workflows
- ask whether to reuse an existing SOP
- render a workflow into a short execution brief
- save or update a workflow after a task is completed

The source of truth is a local workflow library made of JSON files.


## Responsibilities

### Runtime

The runtime side is responsible for:

- workflow matching
- SOP reuse suggestion
- execution brief generation
- workflow draft capture
- workflow save / update

Important runtime rule:

- a matched workflow must not be executed automatically unless the user explicitly asked in the current turn to use the previous SOP or usual process

### UI

The local UI is only for workflow management.

It is responsible for:

- browsing workflows
- editing workflow fields
- saving JSON files

It is not intended to be the main place where runtime matching behavior is exposed.


## Workflow Format

Each workflow is stored as one JSON file.

Example:

```json
{
  "id": "pr-review",
  "name": "PR Review",
  "summary": "Review pull requests with a risk-first pass.",
  "match": {
    "keywords": ["pr", "review", "diff"]
  },
  "steps": [
    {
      "id": "step-1",
      "title": "Step 1",
      "instruction": "Fetch the PR",
      "tool": "github"
    }
  ],
  "tool_preferences": [
    {
      "tool": "github",
      "purpose": ""
    }
  ],
  "version": 1
}
```

Notes:

- `id` is generated from `name`
- step ids are generated automatically
- the current UI stores tool input per step and derives `tool_preferences`


## Main Files

```text
work-style-memory/
├── SKILL.md
├── instruction.md
├── agents/openai.yaml
├── assets/workflow-template.json
├── references/
│   ├── local-ui-spec.md
│   ├── runtime-behavior.md
│   └── workflow-schema.md
├── scripts/
│   ├── capture_workflow.py
│   ├── match_workflows.py
│   ├── new_workflow.py
│   ├── render_workflow_prompt.py
│   ├── save_workflow.py
│   └── workflow_engine.py
└── ui/
    ├── server.py
    └── static/
        ├── app.js
        ├── index.html
        └── styles.css
```


## Core Scripts

### `scripts/workflow_engine.py`

Shared backend logic:

- slug generation
- tokenization
- keyword extraction
- workflow scoring
- matching
- brief rendering
- draft capture

### `scripts/new_workflow.py`

Creates a starter workflow file.

```bash
python3 scripts/new_workflow.py "PR Review" --dir /tmp/workflows
```

### `scripts/match_workflows.py`

Matches a task against saved workflows.

```bash
python3 scripts/match_workflows.py \
  "Please review this PR and look for regressions" \
  --dir /tmp/workflows \
  --tools git,github
```

### `scripts/render_workflow_prompt.py`

Renders a workflow into a compact execution brief.

```bash
python3 scripts/render_workflow_prompt.py \
  /tmp/workflows/pr-review.json \
  --task "Please review this PR and look for regressions"
```

### `scripts/capture_workflow.py`

Creates a workflow draft from a real task description.

```bash
python3 scripts/capture_workflow.py \
  "Triage new bug reports" \
  --steps $'Read issue\nDecide severity\nPropose next action' \
  --tools github
```

### `scripts/save_workflow.py`

Creates or updates a workflow on disk.

Create:

```bash
python3 scripts/save_workflow.py \
  "Review this PR for regressions" \
  --dir /tmp/workflows \
  --steps $'Fetch PR\nInspect risky changes\nWrite findings' \
  --tools git,github
```

Update:

```bash
python3 scripts/save_workflow.py \
  "Review this PR for regressions and test gaps" \
  --dir /tmp/workflows \
  --update pr-review \
  --steps $'Fetch PR\nInspect risky changes\nCheck missing tests\nWrite findings' \
  --tools git,github
```


## UI

Start the local editor:

```bash
python3 ui/server.py --dir ./.openclaw/workflows
```

Then open:

```text
http://127.0.0.1:8765
```

Current UI scope:

- workflow list
- search
- edit form
- JSON preview


## Runtime Behavior

Recommended runtime flow:

1. Before a non-trivial task, check the workflow library.
2. If there is a strong match, ask whether to reuse that workflow.
3. If the user agrees, render the workflow into an execution brief and use it.
4. After the task, ask whether to save or update a workflow.

Important rule:

- do not silently save workflows without user confirmation
- do not silently execute a matched workflow without user confirmation


## Installation

Install by copying the skill folder into the host product's local skills directory.

Example:

```bash
cp -R work-style-memory /path/to/skills/
```

After installation, restart the host product or open a new session/thread.


## Testing

Prepare a test directory:

```bash
mkdir -p /tmp/wsm-test
```

Create a workflow:

```bash
python3 scripts/save_workflow.py \
  "Review this PR for regressions" \
  --dir /tmp/wsm-test \
  --steps $'Fetch PR\nInspect risky changes\nWrite findings' \
  --tools git,github
```

Match a similar task:

```bash
python3 scripts/match_workflows.py \
  "Please review this PR and look for regressions" \
  --dir /tmp/wsm-test \
  --tools git,github
```

Render a brief:

```bash
python3 scripts/render_workflow_prompt.py \
  /tmp/wsm-test/pr-review.json \
  --task "Please review this PR and look for regressions"
```

Start the UI:

```bash
python3 ui/server.py --dir /tmp/wsm-test
```


## Notes

- Matching is heuristic and intentionally lightweight.
- The UI and runtime are separated by design.
- Unicode workflow names are supported.


## References

- `SKILL.md`
- `references/runtime-behavior.md`
- `references/workflow-schema.md`
- `references/local-ui-spec.md`
