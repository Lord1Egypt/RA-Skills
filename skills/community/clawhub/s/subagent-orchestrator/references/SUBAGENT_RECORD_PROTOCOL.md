# SUBAGENT_RECORD_PROTOCOL

Subagent return protocol used together with `subagent-orchestrator`.

## Required header fields

Every subagent return should start with:

- `tag:` `autopilot | done | idle | blocked | handoff | need_user`
- `line:` task-line name such as `ui-autopilot`, `code-autopilot`, `scout-art`
- `node:` current task-line node id such as `code-n4`, `ui-n5`
- `goal_status:` `partial | complete | waiting | blocked`
- `next_role:` free-form next owner/role label such as `ui`, `code`, `verify`, `research`, `archive`, `user`, `none`, or project-specific names

Do not invent extra status values like `half_done`, `in_progress`, or `done` under `goal_status`.

## Short report body

After the header, keep the body short and structured:

1. Goal
2. Completed
3. Changed files
4. Current status
5. Next
6. Risk

## Recommended template

```md
tag: autopilot
line: ui-autopilot
node: ui-n4
goal_status: partial
next_role: verify

## [Subagent] Task record

### Goal
- ...

### Completed
- ...
- ...

### Changed files
- path/a
- path/b

### Current status
- ...

### Next
1. ...

### Risk
- ...
```

## Tag meanings

- `autopilot`: this round is done, but the line probably continues
- `done`: the whole line is complete
- `idle`: waiting for another line or condition
- `blocked`: cannot safely continue automatically
- `handoff`: this round is done and the next role is already clear
- `need_user`: user decision is required

## Controller expectation

The main controller should not treat a finished round as a finished line.
If `tag=autopilot` and the task-line has not reached `end_node`, the controller should continue dispatching the next node.
