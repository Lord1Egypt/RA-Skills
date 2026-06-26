---
name: rr-renamer
description: Use RenameRegex (RR.exe) as a generic Windows CLI bulk renamer from OpenClaw. Use when you need regex search/replace renames with preview (/p pretend), recursive renames (/r), files/dirs selection, and a safe preview→apply workflow. This skill provides a thin wrapper and logging; it does NOT define any specific normalization rules.
disable-model-invocation: true
---

# RR (RenameRegex) generic runner

## Assumptions

- `RR.exe` (RenameRegex) is available on PATH **from the environment that runs the command**.
  - User stated it is placed in `~/.local/bin`.
- Prefer running via **Windows PowerShell 7** (`pwsh.exe`) so Windows path semantics are authoritative.

## Safety defaults

- Always run **pretend preview first** (`/p`).
- Only run apply after **explicit user approval** in the chat.
- Never use `/f` (force overwrite) unless the user explicitly asks.
- Log every invocation.

## How to use

Use the bundled script to run RR.exe inside a chosen root folder.

- Preview:
  - provide RR arguments, script adds `/p` automatically
- Apply:
  - provide RR arguments, script runs without `/p`

See: `scripts/rr_run.ps1`

### Regex argument quoting (PowerShell)

When calling from PowerShell, pass regex arguments like `\s+` as a *single backslash* string.
Recommended: use **single quotes** to avoid accidental escaping:

- `@('*', '\s+', '_', '/r', '/e')`
