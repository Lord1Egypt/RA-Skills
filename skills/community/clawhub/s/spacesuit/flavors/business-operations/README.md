# Business operations flavor 1.0.0

A reusable, opt-in composition of `spacesuit.intel`, `spacesuit.pipeline` and
`spacesuit.monetization` 1.0.0. It selects existing workspace data; it does not
create examples in a real workspace, install background jobs, or configure accounts.

Requires Node.js 18 or later and a Command Center build supporting extension
contract version 1. Command Center remains independently usable without Spacesuit.
Spacesuit is its highly recommended companion, but **Spacesuit alone has no
human-agent interaction UX**. The CLI creates configuration and read-only snapshots;
Command Center supplies the dashboard UI. This does not add a chat composer.

## Preview, select, explicitly collect

Run from the package root, or use the installed package script's absolute path.
Use an absolute, real workspace path (not a symlink). No shell commands are loaded
from manifests and no package-provided executable is dynamically loaded.

```bash
node scripts/flavors.js preview --workspace /path/to/workspace
node scripts/flavors.js apply --workspace /path/to/workspace
node scripts/flavors.js collect --workspace /path/to/workspace
```

For a named instance, add `--profile work --agent main` to **every** operation.
These values must match Command Center's `OPENCLAW_PROFILE` and `OPENCLAW_AGENT`.
The CLI deliberately does not infer identity from the shell environment. Empty
profile and agent `main` are the defaults. Each flavor-enabled instance requires a
distinct workspace: a foreign profile/agent selection, snapshot or backup is
rejected rather than overwritten. This is not filesystem access control between
OS users; use appropriate OS permissions for private workspaces.

Preview prints the before/after selection and writes nothing. Apply preserves
unknown selection metadata and writes `state/command-center/extensions.json`.
The command returns a backup filename for every actual selection change. Review
private before/after output locally; it may contain workspace-specific overrides.

Collect reads only reviewed, fixed input conventions:

- Intel: direct `intel/*.md` files, their modification times and first-ten-line
  `Agent`, `Zpracoval` or `Autor` headers.
- Pipeline: matching direct Markdown filenames containing `PIPELINE` or `QUEUE`,
  table totals and statuses (`status`, `stav`, or `email odesílání`).
- Monetization: `intel/MONETIZATION-TRACKER.md`; table columns `Company`/`Firm`/`Firma`,
  `Revenue`, `Milestone`, `Blocker`, `Priority` (case-insensitive). Blank cells and
  escaped pipes retain their positions. Only explicit positive numeric/currency
  amounts count as revenue, not prose such as “100 prospects”.

Snapshots remain private workspace data. Common credential patterns are redacted before snapshot publication, but this is
defense in depth, not a complete secret scanner. Only
point the collector at inputs appropriate to expose to that workspace's dashboard.
Each selected extension reads only its declared input files. An unrelated malformed,
oversized or unreadable note cannot turn a valid tracker or pipeline into an error.
Input strings are data, never HTML or executable commands. English/Chinese labels
travel with the structured snapshots. Domain names/statuses are preserved as data.

## Limits and availability

Inputs: at most 200 directory entries, 100 Markdown files, 256 KiB/file and 1 MiB
total. Symlinks, nonregular selected files, and outside-workspace paths are rejected.
Output: 256 KiB/snapshot, up to 100 visible rows/table and 2048 characters/cell;
summary counts include all parsed rows. Source files are never changed or deleted.
Choose smaller input files if these display limits hide needed detail.

Missing input is `unavailable`, not measured zero. An existing empty Intel directory
is measured empty; missing tracker is independently unavailable. Invalid/oversized
sources publish `error` only for affected extensions without raw paths or exception details. The host derives
staleness after five minutes. Collection is **explicit and manual**: no scheduling
is installed. Each snapshot is atomically replaced; the three snapshots are not a
cross-file transaction. Command Center must not treat them as a single transaction.
A write failure can leave the previous snapshot for any remaining extension.

## Disable, restore, upgrade

```bash
node scripts/flavors.js disable --workspace /path/to/workspace
node scripts/flavors.js restore --workspace /path/to/workspace --backup BACKUP_FILENAME.json
```

Use the actual UUID filename printed by `apply` or `disable`, not the placeholder.
Disabling selects core monitoring with an empty enabled list; explicit collect
then refuses to run. Snapshots and source data remain on disk. Restore validates
identity and compatibility and restores exact previous selection bytes, including recovery from a corrupt current selection, or removes
the selection if none existed. In the latter case the host's legacy default applies
unless `COMMAND_CENTER_MODE=core` overrides it. Restore creates its own undo backup.

Backups live in `state/command-center/backups/`. Only selection state is backed up;
source data and snapshots are not rolled back. Restore an old package selection only
with a compatible package pair. This release ships only version 1.0.0 and rejects
unsupported versions. Upgrade by reviewing a compatible Spacesuit/Command Center
pair, previewing selection, applying, then collecting. Keep the prior packages to
return to their version after restoring selection.

A workspace-local lock rejects concurrent CLI operations. If an interrupted process
leaves `.flavor-lock`, verify no collector is running before removing that empty
lock directory. Do not restart the gateway or a live dashboard as part of selection.
