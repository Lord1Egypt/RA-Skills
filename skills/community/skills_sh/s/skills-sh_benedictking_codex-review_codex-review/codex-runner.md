---
name: codex-runner
version: 1.0.2
author: BenedictKing
description: Independent subtask for executing Lint and codex review with the recommended gpt-5.3-codex config (internal use)
allowed-tools:
  - Bash
context: fork
---

# Codex Runner Sub-skill

> **Note**: This is an internal sub-skill, invoked by the `codex-review` main skill through the Task tool.

## Purpose

Independently execute Lint and `codex review` commands, using `context: fork` to avoid carrying main conversation context and reduce token consumption.

## Received Parameters

Receives complete command chain through Task tool's prompt parameter:

1. **Lint command**: Auto-selected based on project type (go fmt, npm run lint:fix, black, etc.)
2. **Review mode**: `--uncommitted` or `--commit HEAD` or `--base <branch>`
3. **Model config**: `--config model=gpt-5.3-codex --config model_reasoning_effort=high|xhigh`
4. **Timeout**: Controlled through Task tool's timeout parameter (typically 10 min normal, 15 min difficult, 40 min critical)

## Command Examples

```bash
# Go project - Normal task
go fmt ./... && go vet ./... && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=high

# Go project - Difficult / Critical task
go fmt ./... && go vet ./... && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=xhigh

# Node project - Normal task
npm run lint:fix && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=high

# Python project - Normal task
black . && ruff check --fix . && codex review --uncommitted --config model=gpt-5.3-codex --config model_reasoning_effort=high

# Clean working directory - Review latest commit
codex review --commit HEAD --config model=gpt-5.3-codex --config model_reasoning_effort=high

# Review changes relative to main branch
codex review --base main --config model=gpt-5.3-codex --config model_reasoning_effort=high
```

## Execution Flow

1. **Lint First**: Execute static analysis tools to fix formatting issues first
2. **Codex Review**: Execute code review only after lint succeeds

## Output Format

Returns complete output directly, including:

- Lint tool fix results
- Code review summary
- List of issues found
- Improvement suggestions

## Important Notes

- Must be executed in git repository directory
- Ensure codex command is properly configured and logged in
- Timeout is controlled by the caller through the Task timeout parameter
- Commands are chained with `&&`, so lint failure will stop the subsequent codex review
