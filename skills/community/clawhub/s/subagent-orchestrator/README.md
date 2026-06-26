# subagent-orchestrator

Version: 1.0.0

A lightweight orchestration skill for OpenClaw subagent workflows.

## What it does
- Treats `autopilot` as a continuous task line instead of a one-shot run
- Requires structured subagent return headers: `tag / line / goal_status / next_role`
- Helps the main controller decide whether to continue, hand off, wait, block, or finish
- Encourages cleaning finished sessions while preserving durable memory records

## Return protocol
Subagents should return these headers before the short report:
- `tag:` `autopilot | done | idle | blocked | handoff | need_user`
- `line:` task-line name
- `goal_status:` `partial | complete | waiting | blocked`
- `next_role:` free-form next owner/role label

## Notes
- This skill is intentionally generic.
- Project-specific role defaults and collaboration rules should live in project memory or task boards, not in the skill itself.
