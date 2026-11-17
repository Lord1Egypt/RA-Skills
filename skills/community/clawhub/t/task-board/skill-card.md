## Description:

进度任务管理。记录、追踪、汇报任务进度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanklive](https://clawhub.ai/user/tanklive)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a workspace task board, track task status, and generate concise progress reports during agent-assisted work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions and progress notes may persist sensitive project details in workspace files.

Mitigation: Avoid recording secrets or sensitive business details, and review TASKS.md, memory files, and .learnings/ before sharing the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanklive/skills/task-board)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown task board entries and concise progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update TASKS.md, memory/YYYY-MM-DD.md, and .learnings/ in the workspace when tracking task progress.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
