---
name: persona_management
description: Resolve named personas to their reference photos and read/write the user's long-term creative memory.
always_loaded: false
tool_names:
  - resolve_personas
  - manage_memory
---

# Persona & memory

Resolve named personas to their reference photos and read/write the user's long-term creative memory (preferences, named subjects, ongoing projects).

## Tools

- `resolve_personas {names}` — bind named personas to their reference photos and (optionally) voice clips for the current session.
- `manage_memory` — read / write the user's long-term creative memory (preferences, named subjects, ongoing projects).

## Constraints

- A persona-driven request must call `resolve_personas` before any `image_editing` or `video_editing` tool — never assume a name resolves on its own.
