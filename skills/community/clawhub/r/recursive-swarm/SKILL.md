---
name: recursive-swarm
description: "Bounded recursive orchestration for complex tasks that are too large for one agent turn but cleanly decompose into a few independent subproblems. Use for multi-angle research, audits, mixed research+synthesis, or coding projects that benefit from explicit planning, task-tree state, artifact folders, and controlled parallel execution. Keep recursion tight: default max depth 2, hard cap 3, preferred fan-out 2-4, and modest concurrency. Use git worktrees only for coding leaves inside git repos. Do not use for simple one-shot tasks, destructive workflows, or open-ended exploration."
---

# Recursive Swarm

Use this skill to turn one large task into a small, bounded task tree with explicit node state, artifacts, merge points, and audit events.

## Use this workflow

Use recursive-swarm only when all of these are true:

1. The task is too large or messy for one agent turn.
2. The task has at least 2 meaningful subproblems.
3. The outputs can be merged back into one answer, report, or code result.

Do **not** recurse for simple reads, one-shot edits, destructive workflows, or open-ended exploration with no clear output contract.

## Defaults

- Default max depth: **2**
- Hard cap: **3**
- Preferred fan-out per node: **2-4** children
- Hard cap per node: **5** children
- Default concurrency: **2-3** active leaves
- Hard cap concurrency: **5**
- Default max nodes per run: **9**
- Hard cap nodes per run: **15**
- Default workspace mode: **artifact folders**, not git worktrees
- Append-only audit log: **`events.jsonl`**
- Use git worktrees only for `coding` leaves inside a git repo when sibling edits benefit from isolation

## Node types

Assign each node one primary type:

- `research` — extraction, investigation, analysis
- `coding` — implementation, refactor, test work
- `ops` — shell, system, or environment workflows
- `browser` — web/UI automation
- `synthesis` — combine child outputs into one merged result
- `review` — challenge weak claims, reconcile conflicts, prune bad findings

## Execution routing

Route nodes like this:

- `research`, `synthesis`, `review` → subagents
- `coding` → ACP sessions by default; use worktrees only when useful
- `ops`, `browser` → direct tools or a narrowly scoped subagent if needed
- destructive, external, or approval-sensitive nodes → pause and ask before execution

### Quiet child execution (default)

For routine child runs, prefer **silent child completion + parent-owned final delivery**.

That means:
- child sessions do the work
- child results are harvested from session history and/or artifact files
- routine child announce steps should reply exactly `ANNOUNCE_SKIP`
- the parent/orchestrator sends the one final merged answer to the user

Only allow a child announce message to reach the user when:
- the child is blocked
- the child needs approval to continue
- the child hit a major error the parent must surface immediately
- the child itself is the intended final user-facing delivery step

Do **not** let every child produce routine completion chatter in the user channel.

## Atomic vs composite rule

Treat a node as **atomic** when one agent run can finish it without meaningful internal planning.

Examples of atomic nodes:
- extract top travel dates from the indexed threads
- summarize one PDF
- implement one endpoint
- validate one config file

Treat a node as **composite** when it clearly breaks into independent workstreams.

Examples of composite nodes:
- reconstruct a work year from exported messages
- build a feature spanning backend, frontend, and tests
- audit a system and produce remediation steps

If a child split feels artificial or the merge plan is vague, stop decomposing.

## Workflow

### 1) Initialize the run

Create a run folder with `scripts/init_run.py`.

Recommended output layout:

```text
runs/<run-id>/
  tree.json
  events.jsonl
  summary.md
  nodes/
    1/
      spec.json
      notes.md
      result.md
```

### 2) Create the root node

Use `scripts/upsert_node.py` to record the root task and defaults.

Record at minimum:
- id
- parentId
- goal
- type
- depth
- executor
- status
- workspaceMode
- approvalRequired

### 3) Decompose only when worth it

For each composite node:
- split into 2-5 children
- assign node type and executor
- keep child goals concrete
- define how the parent will merge the results
- stop at depth 2 unless there is a strong reason to go to 3

Never recurse just to make the tree look smart.

### 4) Persist state and audit events

Before executing a node:
- mark it `running`
- create or update `nodes/<id>/spec.json`
- note the intended output in `nodes/<id>/notes.md`
- append an event to `events.jsonl`

After executing a node:
- save the result in `nodes/<id>/result.md`
- mark it `completed`, `failed`, or `waiting_for_approval`
- record artifacts and confidence
- append an event to `events.jsonl`

Use these scripts:
- `scripts/upsert_node.py`
- `scripts/mark_node.py`
- `scripts/list_ready_nodes.py`
- `scripts/list_events.py`
- `scripts/merge_results.py`
- `scripts/render_tree.py`

### 5) Execute leaves

Use `scripts/list_ready_nodes.py` to identify executable leaves.

Execution guidance:
- prefer subagents for analysis/synthesis leaves
- prefer ACP for coding leaves
- prefer direct tools for small ops/browser leaves
- keep concurrency modest; avoid flooding the system with low-value leaves
- when spawning routine child runs, instruct them to keep their work in session/artifacts and reply `ANNOUNCE_SKIP` during the announce step unless they are blocked or explicitly responsible for final delivery
- do not clean up or delete child sessions until the parent has harvested the needed results

### 6) Merge upward

When all child nodes under a parent are complete:
- harvest child outputs from child `result.md`, session history, or other saved artifacts
- use `scripts/merge_results.py` to bundle child file results when applicable
- create a parent synthesis or review node if needed
- write the merged result to the parent `result.md`

If a child was run in quiet mode with `ANNOUNCE_SKIP`, treat that as normal. Silence is not failure; it just means the parent owns user-facing delivery.

Use type-aware merge behavior:
- research → combine evidence, themes, and caveats
- coding → combine patches, test notes, and integration risks
- ops → combine findings, risks, and recommended actions
- review → identify weak claims, contradictions, and missing coverage

Do **not** silently average conflicting child outputs. Bubble disagreements up.

### 7) Finish with a skeptical pass

For important runs, add one final `review` node that:
- challenges overconfident claims
- checks whether decomposition went too far or not far enough
- identifies ambiguous results
- tightens the final summary

## Approval gates

Pause and ask before executing any node that would:
- write, edit, move, or delete important files
- install or update software
- restart services
- change config
- send external messages
- perform destructive system actions

Mark these nodes `waiting_for_approval` instead of forcing them through.

## Worktrees

Do **not** use git worktrees by default.

Use a worktree only when all of these are true:
- the node type is `coding`
- the target is a git repo
- sibling coding tasks benefit from isolation
- there is a plausible merge path afterward

Otherwise keep the node in normal artifact-folder mode.

## Stop conditions

Stop decomposing when any of these is true:
- the node is already atomic
- the merge plan is unclear
- decomposition is becoming repetitive
- depth 2 already produced workable leaves
- time/cost budget would be wasted by further splitting
- adding another node would exceed the run budget

## References

Read these only if needed:
- `references/tree-schema.json` — canonical run and node schema
- `references/example-run.md` — example run layout and sample tree
- `references/quiet-mode.md` — quiet child execution pattern using `ANNOUNCE_SKIP`
