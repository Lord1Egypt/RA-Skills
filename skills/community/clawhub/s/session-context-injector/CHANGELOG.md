# Changelog — session-context-injector

## 1.0.0 — 2026-04-03

Initial release.

- 3 message variants: group session refresh, Nissan DM summary, new room / collaborator welcome
- STATUS.md parser: extracts RESUME FROM HERE + Blockers sections
- HTML parse mode for Telegram (safer than Markdown)
- Decision rules, reuse checklist, failure handling
- Extracted from `playbooks/session-refresh/PLAYBOOK.md` Phase 3
- Invocable from: session-refresh, new-project, telegram-collaborator-room playbooks
