---
name: terminal-command-execution
description: Execute terminal commands safely and reliably with clear pre-checks, output validation, and recovery steps. Use when users ask to run shell/CLI commands, inspect system state, manage files, install dependencies, start services, debug command failures, or automate command-line workflows.
---

# Terminal Command Execution

## Overview
Use this skill to run terminal commands with minimal risk and predictable outcomes. Prefer fast inspection, explicit intent checks, and verification after each state-changing step.

## Workflow
1. Clarify goal and scope.
- Infer the exact command target from context (path, service, tool, environment).
- If request is ambiguous and risky, ask one concise clarifying question.

2. Pre-flight checks.
- Confirm working directory and required binaries.
- Inspect current state before changing it (for example `ls`, `git status`, process/listen state).
- Prefer non-destructive probes first.

3. Execute commands incrementally.
- Run the smallest command that advances the task.
- For multi-step tasks, validate each step before continuing.
- Use reproducible commands and avoid interactive flows when non-interactive options exist.

4. Handle failures systematically.
- Read stderr first and identify root cause class: permission, path, missing dependency, syntax, network, or runtime state.
- Apply one fix at a time, then re-run only the affected command.
- If privileged/destructive action is required, request user approval before proceeding.

5. Verify outcomes.
- Check exit status and observable state changes.
- For installs, verify with a version/health command.
- For edits, verify resulting files and behavior.

6. Report clearly.
- Summarize what ran, what changed, and current status.
- Include exact next command only when additional user action is required.

## Safety Rules
- Avoid destructive commands by default (`rm -rf`, force resets, broad chmod/chown) unless explicitly requested.
- Never assume network, permissions, or package managers are available; test first.
- Prefer scoped operations (specific files/paths/services) over global changes.
- Keep secrets out of command output and logs.

## Command Patterns
- Discovery: `pwd`, `ls -la`, `rg --files`, `which <tool>`
- Validation: `<tool> --version`, health/status commands, targeted smoke tests
- Diagnostics: inspect logs/errors first, then adjust one variable at a time
