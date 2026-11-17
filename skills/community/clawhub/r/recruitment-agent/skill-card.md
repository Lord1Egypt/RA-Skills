## Description:

Recruitment Agent helps recruiters manage Boss Zhipin conversations and Feishu talent workflows, including saving candidate profiles, recording decisions, updating records, and scheduling interviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and hiring operators use this skill to coordinate candidate intake, decision tracking, candidate follow-up, and interview scheduling across Boss Zhipin and Feishu/Lark workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read candidate messages and resumes and write recruiting records that may contain personal data.

Mitigation: Use only authorized recruiting accounts and require explicit confirmation before saving or updating candidate records.

Risk: The skill can send candidate messages and create calendar events.

Mitigation: Require human confirmation before outbound candidate messages, user notifications, or calendar creation.

Risk: The heartbeat workflow can create recurring polling jobs that continue checking candidate replies.

Mitigation: Set expiration, ownership tracking, and reliable cancellation for heartbeat jobs before starting them.

Risk: Parallel Boss Zhipin CLI commands can conflict with shared session state.

Mitigation: Run Boss Zhipin OpenCLI commands serially as required by the artifact workflow.

## Reference(s):

- [Recruitment Agent workflow index](artifact/SKILL.md)
- [Save candidate workflow](artifact/references/workflow-2-save-candidate.md)
- [Decision record workflow](artifact/references/workflow-3-decision-record.md)
- [Update candidate workflow](artifact/references/workflow-4-update-candidate.md)
- [Schedule interview workflow](artifact/references/workflow-schedule-interview.md)
- [Calendar availability utility](artifact/references/util-check-calendar.md)
- [Feishu message utility](artifact/references/util-send-feishu-message.md)
- [Heartbeat polling task](artifact/references/heartbeat_task.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate-record updates, message drafts, calendar actions, and recurring reply-check setup.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
