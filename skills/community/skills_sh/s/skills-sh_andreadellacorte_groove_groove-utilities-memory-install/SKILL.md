---
name: groove-utilities-memory-install
description: "Set up memory backend and configuration."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-install

## Outcome

Memory directories are created and ready for use.

## Acceptance Criteria

- `.groove/memory/daily/`, `.groove/memory/weekly/`, `.groove/memory/monthly/`, `.groove/memory/git/` exist
- `.groove/memory/specs/` directory exists (outcome specs; used by `/groove-work-spec`)
- `.groove/memory/learned/` directory exists
- `.groove/memory/docs/` directory exists (reference docs; used by `/groove-work-doc`)
- User is shown the initialized paths

## Constraints

- Memory path is always `.groove/memory/`
- Create directories if they do not exist:
  ```bash
  mkdir -p .groove/memory/daily .groove/memory/weekly .groove/memory/monthly .groove/memory/git .groove/memory/specs .groove/memory/learned .groove/memory/docs
  ```
- Report the initialized paths to user
