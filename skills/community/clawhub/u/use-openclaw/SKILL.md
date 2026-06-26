---
name: use-openclaw
description: Explain how to use OpenClaw in a local environment. Use when the user asks how to find OpenClaw config or workspace files, how to add or inspect skills, how to understand the purpose of AGENTS.md or workspace notes, how to troubleshoot OpenClaw setup issues, or how to complete a common OpenClaw task step by step.
---

# Use OpenClaw

## Overview

Help the user complete common OpenClaw tasks with minimal ceremony.
Start from the local installation, inspect real files before giving advice, and explain the shortest working path.

## Quick Start

Use this workflow unless the user asks for something narrower:

1. Identify the user's real goal: configuration, skills, workspace files, logs, or troubleshooting.
2. Inspect the relevant local files under `~/.openclaw/` before answering from memory.
3. Prefer concrete paths and commands over abstract explanations.
4. If a change is requested, edit the smallest possible file and then validate the result.

## Core Locations

Check these locations first on a normal local installation:

- `~/.openclaw/openclaw.json`: main configuration file
- `~/.openclaw/workspace/`: shared workspace guidance and notes
- `~/.openclaw/workspace/AGENTS.md`: project or workspace behavior rules
- `~/.openclaw/workspace/TOOLS.md`: environment-specific tool notes
- `~/.openclaw/workspace/USER.md`: user preferences and human context
- `~/.openclaw/skills/` and `~/.openclaw/workspace/skills/`: installed or in-progress skills
- `~/.openclaw/logs/`: logs for troubleshooting
- `~/.openclaw/extensions/`: installed extensions and their docs

On Windows, expand `~` to the user's home directory, for example `C:/Users/<name>/.openclaw/`.

## Common Tasks

### Explain the OpenClaw layout

When the user asks where OpenClaw files live or what each file is for:

1. Read the actual files first.
2. Summarize each file in one sentence.
3. Mention only the files relevant to the user's question.

### Guide a user through a task

When the user asks how to do something in OpenClaw:

1. Map the request to one of these buckets:
   - inspect configuration
   - create or edit a skill
   - update workspace instructions
   - troubleshoot a broken setup
2. Show the exact file or command to check first.
3. Give the shortest safe sequence of steps.
4. If a command fails, inspect the error and adjust instead of repeating generic advice.

### Create or edit a skill

When the user wants a new skill:

1. Decide whether it belongs in `~/.openclaw/skills/` or the current workspace.
2. Create a folder named after the skill.
3. Add `SKILL.md` with clear `name` and `description`.
4. Add `agents/openai.yaml` if UI metadata is needed.
5. Keep the skill concise and put detailed material in `references/` only when necessary.

### Troubleshoot OpenClaw

When the user says OpenClaw is not working:

1. Check the exact failing command or screen.
2. Inspect `~/.openclaw/openclaw.json` and the most relevant file under `~/.openclaw/logs/`.
3. If the issue involves a skill or extension, inspect its `SKILL.md`, README, or config before proposing a fix.
4. Prefer local evidence over assumptions.

## Suggested Commands

Use fast inspection commands first:

- `rg --files "~/.openclaw"`
- `rg -n "keyword" "~/.openclaw"`
- `Get-ChildItem -Force "~/.openclaw"`
- `Get-Content -Raw "~/.openclaw/openclaw.json"`
- `Get-Content -Raw "~/.openclaw/workspace/AGENTS.md"`

Adjust path separators for the current shell when needed.

## Response Rules

- Prefer concrete local paths over generic product descriptions.
- Read before editing.
- Keep explanations short and operational.
- If the user only wants to understand OpenClaw, do not change files unnecessarily.
- If the user wants a fix, make the smallest verifiable change and report what changed.
