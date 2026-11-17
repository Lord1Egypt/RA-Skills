## Description:

Connects an agent to Rain Classroom MCP tools for teacher account, class, teaching activity, student-warning, homework, notice, and lesson-reservation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softwolves](https://clawhub.ai/user/softwolves)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and teaching staff use this skill to connect an agent to Rain Classroom services for checking class data, teaching status, student warnings, homework submissions, notice reads, and lesson reservations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Rain Classroom account, class, teaching, student-warning, homework, notice, and lesson-reservation workflows.

Mitigation: Install only for users who intend to grant that access, and use a scoped, revocable secret.

Risk: The included setup scripts configure an MCP connection and may expose credentials in local MCP configuration.

Mitigation: Inspect generated MCP configuration for plaintext credentials and review the setup behavior before running it.

Risk: The security guidance flags unpinned mcporter usage and a silent install report as items needing review.

Mitigation: Pin or inspect mcporter before setup, avoid passing secrets on command lines, and remove or make install reporting opt-in before deployment.

## Reference(s):

- [Rain Classroom MCP Tool Reference](references/api_references.md)
- [ClawHub Skill Page](https://clawhub.ai/softwolves/skills/yuketang-club-liuxinghui)
- [Rain Classroom Skill Secret Setup](https://ykt-env-example.rainclassroom.com/ai-workspace/open-claw-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and MCP tool usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured YUKETANG_SECRET before Rain Classroom MCP tools can be used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
