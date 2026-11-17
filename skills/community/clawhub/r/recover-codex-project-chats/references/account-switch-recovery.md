# Local projects after GPT account switches

Use this route when signing into another GPT identity or workspace hides local projects,
their chat assignments, or the contents of custom sidebar spaces. This is a local metadata
transfer into the current login, not account sign-in or cloud migration. Obtain the user's
authorization for that local transfer; a request to inspect or refresh alone is not consent
to combine another identity's local library.

## Identify the missing layer

Read the current `.codex-global-state.json` and a read-only SQLite snapshot. Newer desktops
keep inactive identity snapshots under `electron-account-renderer-state-v1.inactive`:

- `globals.local-projects` and `globals.thread-project-assignments` retain project/chat membership.
- `atoms.sidebar-custom-sections-v3` retains local project/chat membership in named spaces.
- `state_5.sqlite` can still contain valid `projects` and `project_roots` even when the current
  renderer's local project list is empty. Empty renderer state alone does not prove data loss.

When Codex app tools are available, compare `list_projects` with `list_threads.sections`.
If projects are present and spaces alone are empty, match old local entries to the existing
space by local host-section identity/name. Use `move_project_to_sidebar_section` or
`move_thread_to_sidebar_section`, then read `list_threads` again. Resolve IDs from the current
app listing, preserve current explicit placements, skip unavailable/archived entries, and
exclude old `chatgpt:` items. This live app-tool route requires no offline database repair.

## One-click and command-line recovery

Prerequisites: macOS, Python 3.9+, an already signed-in destination account, readable local
state/database files, and enough disk space to back up the full local recovery set.
The account identity must be unambiguous. A restricted agent environment that cannot query
processes must hand off the prepared launcher to the user; never treat a failed process
query as proof that the app has stopped.

From the installed Skill directory:

```sh
python3 scripts/restore_local_projects.py
python3 scripts/restore_local_projects.py --report /tmp/codex-recovery-preview.json
# Use Cmd+Q to fully quit ChatGPT/Codex, including background app-server processes.
python3 scripts/restore_local_projects.py --apply
```

For repeated account switches, sign in through the app, quit it, then double-click
`scripts/restore-local-projects.command` in Finder. The launcher preserves its Python
sibling and waits for Return to close its result window. Reopen the app after success.

| Option | Meaning |
|---|---|
| No options | Read-only preview using an in-memory database snapshot. Writes no application data or runtime lock. |
| `--apply` | Explicitly restore after the stopped-process check, complete backup, and conflict validation. |
| `--report PATH` | Write a preview summary to an external file. App data and the Skill directory are rejected as destinations. |
| `--backup-dir PATH` | Persistent backup directory; default `~/Documents/Codex/codex-recovery-backups`. Must be outside app data and the Skill. |
| `-h`, `--help` | Show usage without reading application data. |

`CODEX_HOME` optionally overrides the default `~/.codex`. It is an override, not a required
credential. Legacy `codex_project_recovery.sh` supports `diagnose [CSV]`,
`repair-provider SOURCE TARGET`, and `verify`; it shares the Python stopped-process and
full-backup checks. Provider changes still require evidence that both backend labels are
compatible. Provider identifiers contain only ASCII letters, digits, dot, underscore or hyphen.
The optional `CODEX_RECOVERY_BACKUP_DIR` overrides the legacy command's backup root.

Both repair modes share a lock keyed by the canonical Codex home under
`~/.local/state/recover-codex-project-chats/locks/`, independently of the backup location.
Normal completion and handled failures release it. If an abrupt termination leaves an empty
lock directory, first confirm that no recovery task remains, then remove only the reported
empty directory with `rmdir` and retry. Never remove a lock held by another recovery task.

Exit code 0 means preview completed, no changes were necessary, or the local write and
readback completed. Exit code 1 means a recovery error; argparse usage errors return 2.
Read the message to distinguish those outcomes. A successful local write does not establish
that old chats can open or that their content is complete.

## What changes

The helper merges inactive snapshots' local project definitions and known thread assignments
into current state, verifies exact project roots against actual database IDs, fills missing
`threads.project_id`, and updates the local-host catalog cache. It adds missing local sidebar
entries to the current account's spaces, matching existing local database sections. Existing
current project assignments, space placements and pinned entries win.

It preserves the current identity and all inactive snapshots. It never copies cloud project
ownership, cloud conversations/pages, credentials, work queues or file-access grants from
inactive state. Archived chats remain archived. Unknown threads are not created; missing
rollout bodies are counted, not fabricated. Conflicting roots, database membership or an
ambiguous destination sidebar account stops the operation before repair.

Only a small whitelist of local metadata changes. Full atom dictionaries and all other
account settings remain untouched. A local directory left behind by an old cloud project
may retain local membership, but that does not transfer cloud ownership or access.

## Backups and failures

Before any direct write, the helper checks the main app, helpers and Codex processes are
absent, then backs up the entire Codex home and existing Codex/ChatGPT Application Support
directories, excluding Unix sockets and preserving symlinks. APFS cloning is attempted on
macOS; otherwise files are copied. Large recovery sets can take time and disk space.

Timestamped backup directories are private to the current user and may contain local login
material; keep them local. `codex-home/` contains the pre-repair set including SQLite
WAL/SHM and global state. `result.json` records the write/readback status and `ui_verified=false`.

On write failure the helper attempts to restore pre-write database snapshots and state.
If the app restarts or process status becomes unknown, it stops automatic rollback rather
than touching a possibly live database. Any rollback/report failure is reported separately
with the retained backup directory. Quit the app and inspect copies before further repair;
never overwrite new chats with an old full backup. Failed backups never trigger repair.

## Acceptance

After reopening the app, independently check project visibility, chat membership and each
space's entries. Open representative available chats. Report missing body files and skipped
cloud/archived/unavailable entries separately from restored membership. Repeated runs with
complete metadata should be a no-op. Schema compatibility or isolated tests do not replace
this post-restart acceptance.
