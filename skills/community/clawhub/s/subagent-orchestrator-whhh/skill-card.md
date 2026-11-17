## Description:

Coordinates complex agent work by decomposing tasks into plans, spawning subagents, tracking progress in task files, and consolidating outputs, checkpoints, and diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whhh1994](https://clawhub.ai/user/whhh1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to split larger, multi-step work into managed subagent tasks with persistent plans, status files, checkpoints, and final delivery summaries. It is intended for complex research, coding, configuration, and data-gathering workflows that benefit from staged execution and recovery points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad orchestration authority can spawn sessions, run commands, and write task artifacts.

Mitigation: Install only in environments where this level of agent delegation is intended, and review generated plans before subagents run.

Risk: Persistent task files may store sensitive task details under ~/.openclaw/workspace/tasks.

Mitigation: Avoid using the skill for sensitive work unless local storage is acceptable, and clean task workspaces after review.

Risk: Progress and final summaries may be sent through configured external channels.

Mitigation: Confirm channel routing before use and disable or restrict message behavior where the host environment allows it.

Risk: Cron-related capability may create recurring behavior when enabled with companion cleanup workflows.

Mitigation: Review any scheduled tasks before enabling them and remove schedules that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whhh1994/skills/subagent-orchestrator-whhh)
- [whhh1994 ClawHub profile](https://clawhub.ai/user/whhh1994)
- [Path reference](artifact/references/paths.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task plans, status updates, file paths, command snippets, and delivery summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent task artifacts and send progress or final-result messages through the originating channel.]

## Skill Version(s):

2.0.1 (source: server release metadata; source skill frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
