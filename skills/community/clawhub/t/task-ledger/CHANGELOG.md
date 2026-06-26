# Changelog

## 0.3.2

- Added minimum task-level dependency and readiness semantics with explicit `readiness` configuration on new task skeletons.
- Added `successPolicy` support for `all-succeeded`, `fail-fast`, `wait-all`, and `partial-allowed`.
- Added `allowStartWhen` and `allowPartialDependencies` readiness controls.
- Extended `task-ready.py` to report readiness configuration, satisfied dependencies, closed dependencies, and `ready-with-failures` outcomes.
- Extended `task-start-if-ready.py` to start tasks when readiness resolves to `ready` or `ready-with-failures` under the configured policy.
- Kept the first 0.3.2 step narrowly scoped: explicit dependency semantics first, deeper parent-policy inheritance and optional dependency modeling later.

## 0.3.1

- Added minimum parent-task summary aggregation in `task-export.py`.
- Parent task exports now compute child status counts, child readiness signals, and per-child summaries dynamically from `childTaskIds`.
- Added child aggregation output to both `--format short` and `--format markdown` without changing the task schema or persisting derived fields.
- Keeps the first 0.3.1 step narrowly scoped: export-time aggregation first, deeper workflow semantics later.

## 0.3.0

- Repositioned Task Ledger for the OpenClaw 3.7 era as a **durable workflow layer** instead of a platform-gap patch.
- Rewrote README and SKILL positioning around durable task objects, execution bindings, dependency-aware task graphs, and auditable outputs.
- Added explicit guidance for **when to use** and **when not to use** Task Ledger.
- Added a documented **parallel orchestration pattern**: one parent task for orchestration plus one child task per worker.
- Clarified the relationship between Task Ledger and OpenClaw primitives such as ACP, sub-agents, `exec`, and `cron`.
- Established the 0.3 roadmap around workflow-layer semantics, parent/child aggregation, readiness-aware orchestration, and deeper platform integration.

## 0.2.4

- Fixed `task-advance.py` so advancing the final stage clears `stage` instead of producing a redundant `report -> report` transition.
- Preserved the final `nextAction` guidance for explicit close/validation after the last stage completes.

## 0.2.3

- Added reporting schema fields for `short-first`, `normal`, and `detailed` reporting modes.
- Added short-format export in `task-export.py` for chat-friendly updates.
- Added file-backed long report output via `task-export.py --write-report`.
- Stored generated long report paths in task state.
- Synced the published skill package to include reporting-aware workflow support.

## 0.2.2

- Added readiness helper `task-ready.py`.
- Added `task-start-if-ready.py` for readiness-gated task starts.
- Added relation/dependency graph export in Markdown, DOT, and JSON (`task-graph-export.py`).
- Added readiness column to open-task listing.
- Strengthened `task-doctor.py` with scheduling-specific diagnostics.
- Synced the published skill package to include all local control-plane and scheduling enhancements.

## 0.2.1

- Added parent/child task relation fields and task tree view (`task-ls-tree.py`).
- Strengthened dependency and relation checks in `task-doctor.py`.
- Added human-friendly task export (`task-export.py`).
- Added Markdown output mode to `task-resume-summary.py`.
- Improved `task-bind-process.py` with `process.bound` event naming and optional process state.
- Added `--json` and `--strict` support to `task-doctor.py`.
- Added migration helper `migrate-task-020.py` for bringing legacy task files to the 0.2 baseline.

## 0.2.0

- Added richer task schema with lifecycle, blocking, rollback, and notification fields.
- Added recovery helpers:
  - `task-verify.py`
  - `task-resume-summary.py`
  - `task-bind-subtask.py`
  - `task-bind-cron.py`
- Improved `task-events.py` filtering and JSON output.
- Added specialized templates:
  - `restart-openclaw-gateway.example.json`
  - `deploy-service.example.json`
- Added `task.schema.json`.
- Synchronized the published ClawHub skill package with the local toolkit.
- Published `task-ledger@0.2.0`.

## 0.1.1

- Improved discoverability wording.
- Added better search tags for ClawHub.

## 0.1.0

- Initial public release of the task-ledger toolkit.
