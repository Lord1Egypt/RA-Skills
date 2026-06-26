---
skill_bundle: a11y-audit
file_role: reference
version: 1
version_date: 2026-03-03
previous_version: null
change_summary: >
  Added Claude Code-specific instructions for dev-server discovery,
  Preview tool usage, and workspace-local audit context storage.
---

# Claude Code Notes

Use this file only when running the skill in Claude Code.

## Dev Server Discovery

- Check `.claude/launch.json` for project-specific launch targets, URLs,
  and environment hints before inventing a new startup command.
- If Claude Preview MCP tools are available and a local server needs to
  be started, prefer `preview_start` over ad hoc shell commands.
- If `.claude/launch.json`, package scripts, and repo docs disagree,
  report the mismatch before scanning.

## Workspace-Local Context

- Store mutable audit preferences in the target workspace, not in the
  installed skill directory.
- Default path: `.a11y-audit/PROJECT_CONTEXT.md` at the workspace root.
- If the project already keeps accessibility planning docs elsewhere,
  record those paths in the context file instead of duplicating content.

## Practical Guidance

- Prefer the Preview-provided URL when it differs from a guessed
  localhost port.
- Treat `.claude/launch.json` as a project hint, not as proof that the
  app is healthy. Confirm the selected URL responds before running scans.
