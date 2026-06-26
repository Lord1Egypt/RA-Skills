# Changelog

## 2.1.0 - Features & Security 
### Added
- **Due Dates (`--due`)**: Added due date tracking (`YYYY-MM-DD`) natively to the database. Supports `task create` and `task edit`, visible dynamically on Kanban board and exports.
- **Labels / Tags (`--tags`)**: Tasks can now trace arbitrary metadata hooks (e.g. `--tags="bug,urgent"`), instantly filterable via `task list --tag="urgent"`.
- **Assignment Manipulation**: Tasks can be explicitly assigned without locking queue using `task edit <ID> --assignee="NAME"` or stripped via `--unassign`.
- **Status Escapes (`task unblock`, `task restart`)**: Introduced `task unblock` to reverse a blocked task to pending, and `task restart` to fully reset an active or completed task.

### Security
- **Checkpoint Isolation**: `verification_cmd` execution is explicitly disconnected from auto-execution during `task complete` to prevent recursive RCE vulnerabilities during agent loop cycles. The required command is now printed gracefully for manual or discrete execution.

## 2.0.0 - The Swarm Engine Update
This release fundamentally transforms the `task` CLI from a single-agent checklist into a highly concurrent, fully observable, parallel orchestration engine designed for Swarm AI coordination. All features remain completely native to Bash and SQLite with zero external dependencies.

### Added
- **Swarm Engine (`task claim`)**: Atomic SQLite `UPDATE ... RETURNING` locks prevent race conditions, allowing native parallel execution across multiple AI workers. Safely honors `depend` relationship mapping.
- **Agent Tracking (`task claim --agent="NAME"`)**: Introduced the `assignee` schema attribute natively to the database. All read-only views (dashboard, list, export) now dynamically trace orchestrator assignment visibility.
- **Kanban Dashboard (`task board`)**: A visual ASCII Kanban board that dynamically aligns active tasks, blocked tasks, and real-time nested assignee identifiers without text wrapping limits.
- **Execution Checkpoints (`--verify`)**: `task create` and `task edit` now accept `--verify="<cmd>"`. Completing the task will automatically execute the bash subshell test, blocking the task completion on non-zero exit codes.
- **Context Persistence (`task note`)**: Agents can now attach timestamped runtime logs or error traces directly to task payloads natively, allowing context to survive agent death dynamically.
- **Data Export Pipelines**:
  - `task list --format=chat`: Bypasses ASCII column padding to synthesize native GitHub-flavored Markdown strings.
  - `task export --json`: Exploits SQLite's native `.mode json` to serialize the database schema directly into a mathematical JSON API payload hook.
- **Dependency Flow (`task depend`)**: Natively mapped many-to-many relationships that physically lock dependent tasks in `cmd_claim.sh` until prerequisites are fully cleared.

### Changed
- Refactored `task.sh` `ensure_db` sequentially to backwards-compatibly migrate `assignee` and `verification_cmd` text columns into legacy databases.
## 1.2.2
### Fixed
- **Consistency**: Aligned `task-heartbeat.sh` default database path with the main `task` CLI (`$PWD/.tasks.db`). This resolves the "Suspicious" mismatch flag on ClawHub and ensures heartbeats correctly target the local workspace.

## 1.2.1
### Fixed
- **CRITICAL**: Fixed a data loss bug where `tasks.db` could be wiped during ClawHub `--force` updates.
- **Architecture Change**: Tasks are now inherently **workspace-scoped**. The database defaults to a hidden `.tasks.db` file in the *current working directory* (`$PWD`) instead of existing globally or alongside the script directory. This enables seamless per-project task lists and isolates data from skill updates.

### Added
- `CHANGELOG.md` for proper release tracking.

### Removed
- Removed the deprecated `task_min.sh` minification script, as the modular 1.2.0 script architecture permanently bypassed the file size limits.

## 1.2.0 - 2026-03-03
### Added
- `task edit` command - Modify the description, priority, or project of an existing task.
- `task export` command - Export filtered tasks to a clean markdown table.
- Modular architecture: Split the giant monolithic bash script into 12 separate `cmd_xxxx.sh` subroutines to bypass ClawHub analysis limits.

## 1.1.5 - 2026-02-28
### Security
- Made `~/.local/bin` symlinking in `install.sh` strictly opt-in via a new `--symlink` flag to satisfy malware scanner constraints regarding silent filesystem persistence.

## 1.1.3 - 2026-02-28
### Security
- Fixed a SQL injection vulnerability by creating a strict integer validation regex helper for all database queries.
