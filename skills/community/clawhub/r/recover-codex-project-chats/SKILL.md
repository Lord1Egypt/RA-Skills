---
name: recover-codex-project-chats
description: >
  Use when users need to recover missing local Codex/ChatGPT Desktop projects, project chats,
  and sidebar spaces after GPT account or workspace switches. Also use for lost
  local assignments, provider mismatches, archived or invisible histories, moved
  workspace paths, and schema-compatible local backup comparisons.
---

# Recover Codex project chats

- **Version**: 1.1.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills/tree/main/skills/recover-codex-project-chats

Restore project visibility without overwriting the only copy of a conversation.

## Account switches and empty sidebar spaces

Read [references/account-switch-recovery.md](references/account-switch-recovery.md) when
projects disappear after signing into another GPT account, or projects exist but
custom sidebar spaces are empty. Restore local project membership and sidebar membership
as separate layers. Prefer the app's sidebar tools for missing space entries while the
app is running; direct file/database repair requires the stopped application.

For an authorized transfer of local metadata into the current account:

```sh
python3 scripts/restore_local_projects.py
# After reviewing the preview and fully quitting ChatGPT/Codex:
python3 scripts/restore_local_projects.py --apply
```

On macOS the user can double-click `scripts/restore-local-projects.command` after quitting.
It invokes the same guarded restore. Signing in remains an app operation. Never transfer
cloud conversations, cloud project access, credentials, queued work, or file permissions.

## Other recovery workflows

1. Run `scripts/codex_project_recovery.sh diagnose [csv-path]` while Codex may remain open. Save the output.
2. Read `references/incident-patterns.md` and classify the evidence before changing data.
3. Back up current `~/.codex`, the supplied backup, and Codex-related Application Support directories. Exclude only live Unix sockets.
4. Before any direct on-disk mutation, require Codex Desktop to be fully stopped. Confirm the app-server, renderer, and service processes are absent.
5. Run SQLite `PRAGMA integrity_check` on copies first. Inspect `.schema`; never invent columns.
6. Apply only the matching repair:
   - Provider mismatch: run `scripts/codex_project_recovery.sh repair-provider <old-provider> <current-provider>` after explaining the evidence. Repair only when both names refer to the same compatible backend.
   - Missing assignments: rebuild `thread-project-assignments` in `~/.codex/.codex-global-state.json` from actual thread IDs and cwd values. Preserve existing assignments. Resolve overlapping roots and temporary directories explicitly; do not rely solely on prefix matching.
   - Moved paths: create and review an old-cwd to current-project mapping before updating assignments or cwd metadata.
   - Missing database rows: merge only from a schema-compatible backup after integrity checks and a trial on copies.
7. Run `scripts/codex_project_recovery.sh verify` while Codex is stopped, then restart Codex and check each project in the UI.
8. Report root cause, backup paths, CSV rows, database rows, rollout files found, per-project visible counts, changed rows/files, and unrecovered thread IDs.

## Safety rules

- Treat `state_5.sqlite` plus WAL/SHM, rollout JSONL, `~/.codex/.codex-global-state.json`, and project metadata as one recovery set.
- Do not edit a live SQLite database.
- Do not replace all of `~/.codex` when a targeted repair is sufficient.
- Preserve archived state unless the user explicitly requests unarchiving.
- Do not change provider metadata merely to make rows visible unless the configured provider is compatible with the original sessions. Prefer restoring the provider configuration when compatibility is uncertain.
- Keep every pre-repair backup until the user verifies the UI and can open representative chats.

## Resources

- `scripts/codex_project_recovery.sh`: read-only diagnosis, guarded provider repair, and verification.
- `references/incident-patterns.md`: other failure patterns, schema landmarks, and evidence tests.
- `references/account-switch-recovery.md`: account-scoped state, one-click use, CLI options, backup/recovery boundaries, and app verification.
- `scripts/restore_local_projects.py`: preview or restore local projects, chats, and sidebar spaces from local inactive-identity snapshots.
- `scripts/restore-local-projects.command`: macOS double-click restore launcher.
- `tests/test_restore_local_projects.py`: synthetic recovery, isolation, conflict, rollback, and sidebar regressions. Run with `python3 -m unittest discover -s tests -v`.

## Dependencies

- macOS with Codex Desktop or ChatGPT Desktop using the Codex runtime
- Python 3.9+ (standard library only) for account-switch recovery and shared safety checks
- Zsh and `/bin/ps` on macOS; legacy diagnosis/provider commands additionally use SQLite 3, jq, ripgrep, and Perl
- Optional CSV snapshot or `~/.codex` backup for comparison

Version history: [CHANGELOG.md](CHANGELOG.md).
