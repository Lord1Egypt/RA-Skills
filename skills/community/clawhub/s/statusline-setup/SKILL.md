---
name: "statusline_setup"
description: "Use when the user wants to configure Claude Code statusline UI by inspecting shell prompt configuration and updating the relevant settings."
---


# Statusline Setup

Use this skill to configure Claude Code's statusline UI from an existing shell prompt setup.

## Workflow
1. Inspect the shell prompt or statusline context the user wants to mirror.
2. Read existing Claude settings that control statusline behavior.
3. Adjust the settings with minimal changes.
4. Explain what changed and how to refine it further.

## Guardrails
- Inspect current config before editing.
- Make the smallest possible settings change.
- Preserve unrelated user preferences.

## Example Requests
- Set up Claude statusline to match my shell prompt.
- Tune the statusline UI from current shell config.

## Inputs
- Existing shell prompt context
- Current Claude settings

## Outputs
- Updated statusline-related settings
- Refinement notes

## Success Criteria
- The shell context was inspected first.
- Settings changes stayed minimal.
- User preferences were preserved.

## Non-Goals
- Blind statusline config rewrites

## Source Provenance
Derived from `src/commands/statusline.tsx`.
