## Description:

Manage complex long-running tasks with checkpoint files, step tracking, and periodic progress reports until completion or pause.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mashirops](https://clawhub.ai/user/mashirops)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to supervise large, multi-step tasks by creating checkpoint files, tracking step status, and sending periodic progress or blocker summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent `.tasks/` files may retain task details beyond the active work session.

Mitigation: Use the skill only when local task-status retention is acceptable, and define cleanup expectations before using it for sensitive work.

Risk: Recurring external progress messages have unclear destination, consent, retention, and cleanup behavior.

Mitigation: Confirm the reporting channel and recipient consent before activation, and verify scheduled reporting is removed when the task completes or fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mashirops/skills/task-supervisor)
- [ClawHub publisher profile](https://clawhub.ai/user/mashirops)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown task files with shell command snippets and brief text status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent task files and scheduled external progress reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
