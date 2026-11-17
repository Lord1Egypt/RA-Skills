---
name: "repository-janitor"
description: "Audit Git repositories and worktrees, preserve findings, and monitor scheduled audit health without deleting work."
---

# Repository Janitor

A conservative Linux repository auditor with a deterministic Python executor, private finding history, and an optional OpenClaw scheduler watchdog.

## Workflow

1. **Define the inventory.** Read applicable project instructions and [references/configuration.md](references/configuration.md). Create a private configuration based on [references/repositories.example.json](references/repositories.example.json). List only repositories the operator has authorized. Keep runtime checkout and administrative Git checkout separate. **Done:** each target has a verified identity and scope; examples are not treated as installed configuration.
2. **Run the audit.** From this skill directory, run:
   ```bash
   python3 scripts/audit.py --config /absolute/path/to/private-config.json --fetch --github --persist --report
   ```
   The executor owns its lock. Do not acquire it again or run a second fetch around this command. Omit `--fetch`, `--github`, or `--persist` when those actions are not requested; omitted network checks remain explicitly unknown. **Done:** a report or an explicit execution failure is available.
3. **Interpret the result.** Read [references/findings.md](references/findings.md). Separate successful execution from repository cleanliness. Preserve open findings when coverage is incomplete. A clean index is not proof that PRs, commits, or worktrees need no attention. **Done:** coverage, evidence, open findings, and unknown checks are stated separately.
4. **Handle any requested organization manually.** The Python executor implements only `AUDIT`. For `ORGANIZE_SAFE` or `PREPARE_CLEANUP`, follow [references/supervised-actions.md](references/supervised-actions.md) under explicit authorization for that run. **Done:** approved actions have preconditions, verified backup, and postconditions; other targets remain untouched.
5. **Configure monitoring only when requested.** Read [references/scheduling.md](references/scheduling.md). Test execution and delivery independently. Do not overwrite an existing job whose owner or authority cannot be verified. **Done:** schedule, destination, owner, and watchdog behavior have been checked, or the activation blocker is reported.
6. **Validate changes.** Run `python3 -B scripts/test_audit.py`. Use temporary repositories for tests, not production changes. Confirm that only the current run's lock was released. **Done:** focused tests pass and a partial audit is never described as a successful complete audit.

## Requirements and effects

- Linux, Python 3, Git, and readable `/proc` for process observations.
- GitHub CLI (`gh`) with separately configured authentication for `--github`.
- Optional systemd/SQLite runtime checks require the explicit runtime fields documented in the configuration reference.
- OpenClaw CLI is required only for the optional scheduler watchdog.
- The audit reads Git metadata, worktree status, filesystem metadata, and optional runtime/database signals. It does not read changed-file contents.
- `--fetch` performs `git fetch --prune` against the configured remote: remote-tracking refs can change, but working files are not updated.
- The executor creates an exclusive run marker at the configured lock path, then removes only its own marker. An existing marker is preserved, even if it looks stale.
- `--persist` writes private JSON state atomically. A corrupt baseline blocks replacement. Keep state outside the skill, source repositories, indexed memory, and public artifacts.
- Optional process environment inspection selects only the configured database directory key and never emits the environment contents.
- A read-only SQLite connection runs `PRAGMA quick_check` with an interrupt deadline; no migrations, vacuum, or business-row queries are executed.

## Modes

### AUDIT — default and only automated mode

Inspect repositories and report risks. No cleanup, automatic commits, fast-forward, deployment, or pruning of worktree registrations. A successful process exit indicates that a report was produced: inspect its `errors` and findings before claiming complete coverage.

### ORGANIZE_SAFE — explicit authorization for one supervised run

Allows only verified pruning of administrative records for genuinely missing worktree directories, or a verified fast-forward of a clean non-runtime checkout. This is a manual workflow, not a CLI flag. Existing dirty, locked, or active worktrees remain untouched.

### PREPARE_CLEANUP — explicit authorization

Identify exact targets and prepare verified backups. Do not delete or overwrite targets. Actual material cleanup requires a separate supervised authorization for those exact targets.

## Permanent automated limits

The scheduled auditor never deletes code, untracked files, branches, tags, worktrees, caches, builds, backups, releases, runtime dependencies, databases, uploads, credentials, or logs. It never performs `git clean`, automatic stash, reset, rebase, force push, commit, push, PR mutation, operation continuation/abort, process termination, migration, restart, or deployment.

Age, size, inactivity, absent approval, and a clean Git status never authorize deletion. A free persistent deployment lock is normal and is not removed.

## Coverage boundaries

- Worktrees are inspected individually; registered repositories sharing a common Git directory are deduplicated.
- Process observations use readable process working directories, not a complete attribution system. Partial visibility is reported in observations; absence of a PID does not prove inactivity.
- WIP age is based on available dirty-path mtimes, not the moment the worktree became dirty. Pure deletions can have unknown age. Automation ownership and handoffs require external evidence.
- PR listing is bounded to 100 results; reaching the limit is incomplete coverage. Review threads are not queried by this version. Draft status and missing approval are not defects by themselves.
- Discovery and artifact measurements are bounded metadata inventories, not licenses to clean.
- A watchdog on the same host/Gateway is not an external server availability monitor.

The public package contains examples only: no publisher deployment paths, scheduler IDs, account credentials, repository history, or operational findings.
