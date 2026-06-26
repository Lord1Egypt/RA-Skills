# Run Readiness

TaskOps classifies every task node before it enters execution.
Execution happens in independent run graphs under `runs/<run-id>/` and should remain bidirectionally traceable to the source task when the run originates from a task.

## Values

### `runnable`

The task can move to the run graph now.

Minimum conditions:

- input is clear
- output is clear
- success can be judged
- responsibility is singular
- running it will not change the meaning of downstream tasks

### `needs_decomposition`

The task is too large for a single run, and the system understands the domain well enough to split it into child responsibility units.

This is not the same as “large”. Decomposition requires knowledge.

### `needs_exploration`

The task objective is meaningful, but TaskOps does not yet understand the inner structure well enough to decompose or execute honestly.

This is the unknown-unknowns state.

Exploratory runs may include:

- search
- source reading
- small prototype
- tool/API trial
- debug attempt
- try/error loop
- retrospective

The output is not “task completed”. The output is understanding that enables the next decomposition or execution decision.

Required exploratory run output:

- learned facts
- discovered constraints
- failed/successful approaches
- remaining unknowns
- recommended next decomposition or runnable task

### `blocked`

The task cannot progress until an external dependency, missing input, permission, or decision is resolved.

If the dependency has been intentionally handed to a human, another AI, an agent, or an external system, represent that in the run graph as a delegated waiting node rather than hiding it inside a vague blocker.

## Recommended task frontmatter

```yaml
runReadiness: needs_exploration
runReadinessReason: We do not yet know whether the API supports the required state transition.
understandingLevel: partial
unknowns:
  - API behavior under retry
  - exact validation constraints
nextLearningGoal: Try a minimal API call and summarize the constraints needed for decomposition.
```

Optional confidence fields:

```yaml
decompositionConfidence: 0.4
executionConfidence: 0.2
```

## CLI

```bash
taskops classify-runnable <work-dir> <task-id>
taskops classify-runnable <work-dir> <task-id> --json
```

The command returns the current readiness, reason, and next action:

- `send_to_run_graph`
- `decompose_task_group`
- `create_exploratory_run`
- `resolve_blocker`

## Delegated waiting in the run graph

Delegation is execution truth, not decomposition truth.

When a runnable/exploratory task requires someone else to produce an output, create a run node like:

```yaml
entityType: runNode
type: delegate
status: waiting
delegateeType: human|ai|agent|system
delegateeRef: jimmy
request: The concrete ask.
expectedOutput: The exact output needed before downstream execution continues.
requestedAt: 2026-05-08T04:45:00+09:00
timeoutAt: 2026-05-10T04:45:00+09:00
sourceTaskId: task-user-constraints
sourceTaskGroupVersionId: tgv-root-v1
```

Downstream run paths should not continue until the delegated node is resolved, cancelled, or timed out into an explicit follow-up.

## Runner dispatch table

`taskops run` does not only consume `runnable` tasks. Each step picks the next non-`done`/`cancelled` task in active snapshot order and dispatches based on the classification:

| Classification        | Runner action                                                                                                                                            |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `runnable`            | Execute via the executor; mark task done; attach task + run EoW; write the `closes_with` edge.                                                           |
| `needs_decomposition` | Open a `type: decomposition` run node; expand the task graph (child task group + v1 version); set parent `childTaskGroupId`; close parent with EoW reason `decomposed_by_runner`. The runner also extends the active snapshot's `selectedVersions` with the new child task group/version so the new children become visible to later steps of the same runner invocation. |
| `needs_exploration`   | Open a `type: exploration` run node; write a reflection artifact at `runs/<run-id>/artifacts/<run-node-id>.md`; close parent with EoW reason `exploration_recorded_by_runner` and set `runReadiness: needs_decomposition`. |
| `blocked`             | Skip unless declared `blockedBy` references have all resolved; then reopen the task before selection. If only unresolved blocked tasks remain, the runner stops with `blocked_only`. |

Before each selection pass, the runner rechecks `blockedBy` references. A blocker can point at a task (`type: task`, `id`, optional `taskGroupVersionId`) or a run node (`type: runNode`, `runId`, `id`). When all blockers are `done` or `cancelled`, the task is reopened with `status: pending`; `runReadiness: blocked` is cleared unless `unblockRunReadiness` provides the next readiness.

Additionally, the runner pauses immediately when it encounters a `status: waiting` task or non-delegate run node, or a `type: delegate` run node that is not `done`/`cancelled`. Delegate type wins over generic waiting, so `type: delegate` + `status: waiting` reports `delegation_pending`.

Dry-run decomposition synthesizes a single `runReadiness: blocked` placeholder child marked `Synthetic dry-run placeholder. A human must supply real inputs before this becomes runnable.` so it cannot be mistaken for real progress. Dry-run exploration writes a deterministic reflection artifact with the same caveat.

### Optional self-delegate loopback

Pass `--loopback self --max-loopbacks <n>` (default `n=3`) to let the runner auto-resolve *self-delegate* run nodes (`delegateeType: self`, `delegateeRef: self`, or `delegateeRef: <work-id>`) instead of stopping with `delegation_pending`. For each pending self-delegate the runner opens a `type: loopback` resolution node (`run-node-loopback-<delegate-id>[-<n>]`), writes a `loopback` edge to it, executes the loopback (dry-run synthesises an artifact; `openclaw-agent` dispatches a fresh single-step agent), then closes the loopback (EoW reason `loopback_recorded`) and the original delegate (EoW reason `self_loopback_resolved`, with `resolvedBy: self_loopback` and `resolvedByRunNodeId` on the delegate). Each loopback counts against `--max-steps` *and* the loopback budget. Non-self delegates still stop with `delegation_pending`. Default `--loopback none` keeps the pre-existing pause behaviour.

## Terminal stop reasons

`taskops run` reports one of these when it cannot start a new step:

- `all_closed` — the selected work is fully closed: every terminal task is closed by task EoW, every run terminal node is closed by run EoW, and no waiting/delegated/blocked work remains. This is the closure-complete terminal state.
- `no_runnable` — nothing is actionable but the work is not yet closed (terminal EoW coverage incomplete or otherwise inconsistent). Inspect rather than treat as success.
- `blocked_only`, `waiting`, `delegation_pending` — open work parked on blockers/wait/delegation; resolve before continuing.
- `max_steps`, `deadline_reached` — safety caps stopped the run before further work could begin and take precedence over `all_closed` / `no_runnable`.
- `max_loopbacks` — the `--max-loopbacks` budget is exhausted while a self-delegate is still pending; raise the budget, resolve manually, or invoke `taskops run` again to spend more loopbacks.
- `task_failed`, `validation_failed` — executor failure or mid-run re-parse error.

## Restarting from a task

`taskops restart <work-dir> --from <task-id> --instruction "<text>" [--reason <text>] [--instruction-file <path>] [--json]` rolls the active selected version forward to a new version that re-executes from `<task-id>`. Use it instead of editing `status: done` back to `pending`:

- Upstream tasks (`order < target.order`) keep their status; done leaves get a fresh EoW with `reason: preserved_upstream_after_restart`. Each preserved task carries `preservedUpstream: true` and `preservedFromVersionId`.
- The target task is reset to `pending` and gains `restartInstruction`, optional `restartReason`, `restartedFromVersionId`, and `restartedAt`.
- Downstream tasks (`order >= target.order`, excluding the target) are reset to `pending`.
- The prior version is rewritten with `selected: false` and `supersededByVersionId`. The active snapshot's `selectedVersions` is repointed at the new version and the parent task group's `activeVersionId` follows if it pointed at the prior. Historical run nodes/EoWs/edges remain unchanged.
- Restart refuses if the project has validation errors or if `<task-id>` is missing from / ambiguous across selected versions.
