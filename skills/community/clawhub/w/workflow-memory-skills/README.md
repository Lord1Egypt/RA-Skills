# Work Style Memory

Turn repeated multi-step tasks into reusable local workflows for Codex, OpenClaw, or similar agent runtimes.

## 中文简介

`work-style-memory` 是一个把“你的做事方式”沉淀成本地 workflow / SOP 的 skill。

它适合这样的场景：

- 你经常让 agent 处理同类多步骤任务
- 你希望 agent 先检查有没有现成 SOP，而不是每次从头开始
- 你希望 agent 在执行前先问一句“发现已有流程，是否复用？”
- 你希望任务做完后，可以把这次过程保存成新的 workflow，或者更新旧 workflow

这个项目把 workflow 存成可编辑的本地 JSON 文件，并提供：

- runtime 侧的匹配、复用确认、brief 生成、保存与更新
- 本地 UI 侧的浏览、编辑、删除、预览

## Overview

`work-style-memory` is a local skill for turning repeated multi-step tasks into reusable workflows.

It helps an agent:

- detect when a new task looks similar to a saved SOP
- ask whether to reuse that SOP before execution
- render a workflow into a short execution brief
- save or update a workflow after a task is completed

The workflow library lives in local JSON files so it can be safely edited by scripts, the UI, or the user directly.

## UI Preview

![Work Style Memory UI](./assets/ui-screenshot.png)

## Core Ideas

- Workflows are structured memory, not giant prompts.
- A matched SOP should be suggested first, not silently executed.
- The UI is for editing workflow files, not for simulating runtime chat behavior.
- The workflow file is the source of truth.

## Features

- workflow matching for repeated tasks
- explicit confirmation before reusing a matched SOP
- workflow-to-brief rendering for runtime execution
- draft capture and save / update after real tasks
- local UI for browsing, editing, deleting, and previewing workflows
- Unicode-friendly workflow names and file paths

## Runtime Behavior

Recommended flow:

1. Before a non-trivial repeated task, check the saved workflow library.
2. If there is a strong match, ask the user whether to reuse it.
3. If the user agrees, compile the workflow into an execution brief and run with it.
4. After the task, ask whether to save a new workflow or update an existing one.

Important rule:

- Do not silently execute a matched SOP unless the user explicitly asked to use their previous workflow in the current turn.

## Workflow Format

Each workflow is stored as one JSON file.

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

## Quick Start

Create a workflow:

```bash
python3 scripts/new_workflow.py "PR Review" --dir /tmp/workflows
```

Match a task:

```bash
python3 scripts/match_workflows.py \
  "Please review this PR and look for regressions" \
  --dir /tmp/workflows \
  --tools git,github
```

Render an execution brief:

```bash
python3 scripts/render_workflow_prompt.py \
  /tmp/workflows/pr-review.json \
  --task "Please review this PR and look for regressions"
```

Save a workflow from a real task:

```bash
python3 scripts/save_workflow.py \
  "Review this PR for regressions" \
  --dir /tmp/workflows \
  --steps $'Fetch PR\nInspect risky changes\nWrite findings' \
  --tools git,github
```

## Local UI

Start the editor:

```bash
python3 ui/server.py --dir ./.openclaw/workflows
```

Then open:

```text
http://127.0.0.1:8765
```

The UI is intentionally scoped to workflow management:

- browse workflows
- edit workflow fields
- delete workflows
- preview JSON

Runtime matching and reuse prompts should happen in the agent conversation flow, not inside the editor.

## Installation

Copy the folder into your host product's local skills directory and restart the host or open a new session.

```bash
cp -R work-style-memory /path/to/skills/
```

Typical workflow storage locations:

- project-local: `./.openclaw/workflows`
- personal global store: `$CODEX_HOME/work-style-memory/workflows`

## Project Structure

```text
work-style-memory/
├── SKILL.md
├── instruction.md
├── assets/
├── references/
├── scripts/
└── ui/
```

## Documentation

- [instruction.md](./instruction.md)
- [references/workflow-schema.md](./references/workflow-schema.md)
- [references/runtime-behavior.md](./references/runtime-behavior.md)
- [references/local-ui-spec.md](./references/local-ui-spec.md)

## License

[MIT](./LICENSE)
