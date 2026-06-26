# Gap Analysis: `team-tasks` vs Official Claude Code Agent Teams

Date: 2026-02-08

## Scope
Compared these files:
- `AGENT_TEAMS_OFFICIAL_DOCS.md`
- `SKILL.md`
- `scripts/task_manager.py`
- `SPEC.md`

This analysis compares our current implementation to official Claude Code Agent Teams behavior, not just to our internal spec.

## Summary Table
| Capability | Official Claude Code Agent Teams | Current `team-tasks` | Gap | Assessment |
|---|---|---|---|---|
| Team model (lead + teammates as managed instances) | Built-in team lead + spawned teammates with independent contexts | No native team object or spawn lifecycle in `task_manager.py`; project JSON tracks tasks/debaters only | High | We have a task tracker, not a full team runtime |
| Direct teammate communication (`message`, `broadcast`, mailbox) | Teammates can message each other directly | `SKILL.md` explicitly states centralized orchestration: "agents never talk to each other directly" | High | Core architectural mismatch |
| Shared task list with self-claim | Teammates self-claim or are assigned; shared list for all agents | Lead/dispatcher updates statuses; no claim command for teammates | High | Centralized control only |
| Race-safe task claiming (file locking) | Explicit locking for claim operations | No locking primitives or claim workflow in script | High | Concurrency safety missing for multi-writer use |
| Dependency handling / unblock | Dependencies and automatic unblock | Implemented via DAG `dependsOn` + `ready` + unblocked notifications (`compute_ready_tasks`, `cmd_update`) | Low | Strong match |
| Task state lifecycle | `pending`, `in progress`, `completed` | `pending`, `in-progress`, `done`, plus `failed`, `skipped` | Low | Equivalent + extensions |
| Delegate mode (lead restricted to orchestration tools) | Supported | Not implemented | High | No guardrails for lead behavior |
| Plan approval workflow | Teammates can be forced to submit plans for approval | Not implemented | High | Missing governance loop |
| Quality gates / hooks (`TeammateIdle`, `TaskCompleted`) | Supported with blocking feedback | Not implemented | High | Missing policy enforcement points |
| Display modes (in-process, split panes) | Supported | Not implemented in this tool | Medium | Mostly UX/runtime gap |
| Data model for teams | Team config + members persisted in `~/.claude/teams` and task list in `~/.claude/tasks` | Project JSON only (`/home/ubuntu/clawd/data/team-tasks/*.json`) | Medium | Simpler model; lacks team/member metadata |
| Project context propagation | Teammates load same project context automatically | Workspace path is manually stored and surfaced via `--workspace`, `next`, `ready` | Medium | Useful, but not full context/session semantics |
| Debate / competing hypotheses workflow | Documented as use case pattern | Dedicated `debate` mode with `add-debater` + `round` actions is implemented | Positive delta | Feature extension beyond official baseline tooling |
| Cross-review prompt generation | Not a dedicated first-class command in official docs | Implemented in `round <project> cross-review` | Positive delta | Good specialized workflow |

## Evidence Highlights
- Official direct teammate messaging and mailbox features: `AGENT_TEAMS_OFFICIAL_DOCS.md:35`, `AGENT_TEAMS_OFFICIAL_DOCS.md:36`, `AGENT_TEAMS_OFFICIAL_DOCS.md:37`.
- Official claim locking and dependency unblock semantics: `AGENT_TEAMS_OFFICIAL_DOCS.md:45`, `AGENT_TEAMS_OFFICIAL_DOCS.md:46`.
- Official delegate/plan approval/hooks/display modes: `AGENT_TEAMS_OFFICIAL_DOCS.md:48`, `AGENT_TEAMS_OFFICIAL_DOCS.md:53`, `AGENT_TEAMS_OFFICIAL_DOCS.md:60`, `AGENT_TEAMS_OFFICIAL_DOCS.md:63`.
- Current architecture is centralized by design: `SKILL.md:10`, `SKILL.md:11`.
- Current implementation does include debate + workspace enhancements from spec: `scripts/task_manager.py:992`, `scripts/task_manager.py:995`, `scripts/task_manager.py:1007`, `scripts/task_manager.py:1013`, `scripts/task_manager.py:746`, `scripts/task_manager.py:708`.
- Internal spec goals for debate/workspace: `SPEC.md:16`, `SPEC.md:57`.

## Honest Assessment
`team-tasks` is a solid JSON-based orchestration layer for linear and DAG pipelines, and now includes a useful debate workflow. It is effective for AGI-centric dispatch where one coordinator drives all state transitions.

It is **not yet close to full parity** with official Claude Code Agent Teams runtime semantics. The biggest gaps are architectural: no teammate-to-teammate mailbox, no self-claim/locking model, and no delegate/approval/hooks governance features. In practical terms, this behaves more like a workflow/state manager than a true multi-agent team runtime.

## Priority Gaps to Close (if parity is the goal)
1. Add a first-class team/member runtime model with explicit lead + teammate identity and lifecycle.
2. Implement mailbox primitives (`message`, `broadcast`, inbox/outbox) so teammates can coordinate directly.
3. Add claim/release semantics with lock-safe updates to prevent race conditions.
4. Add governance features: delegate mode restrictions, plan approval state machine, and completion/idle hooks.
5. Align docs (`SKILL.md`) with actual capabilities (`debate`, `workspace`) to remove drift.
