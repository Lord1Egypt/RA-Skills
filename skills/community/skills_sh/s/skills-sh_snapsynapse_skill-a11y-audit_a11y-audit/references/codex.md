---
skill_bundle: a11y-audit
file_role: reference
version: 1
version_date: 2026-03-03
previous_version: null
change_summary: >
  Added Codex-specific instructions for workspace-local state,
  dependency checks, and dev-server discovery without Claude tools.
---

# Codex Notes

Use this file only when running the skill in Codex.

## Dev Server Discovery

- Check `package.json`, repo docs, and existing running processes first.
- Treat `.claude/launch.json` as an optional repo artifact if it exists;
  do not assume Claude Preview tooling is available.
- If the workspace contains multiple frontend apps, identify the target
  app before scanning or state the assumption explicitly.

## Workspace-Local Context

- Store mutable audit preferences in the target workspace, not in the
  installed skill directory.
- Default path: `.a11y-audit/PROJECT_CONTEXT.md` at the workspace root.
- Reuse an existing project-local context file when present; otherwise,
  create the default file only after confirming the audit scope.

## Practical Guidance

- Ask before installing missing packages such as `axe-core`,
  `puppeteer`, `playwright`, or `lighthouse`.
- Prefer project-local commands and dependencies over global tooling.
- If browser automation is blocked by missing dependencies or a missing
  running app, summarize the blocker and continue with the highest-value
  partial audit the workspace supports.
