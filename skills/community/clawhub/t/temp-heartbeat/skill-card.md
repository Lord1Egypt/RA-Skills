## Description:

Temp Heartbeat lets agents create one-time temporary heartbeat tasks that run at a specified time and delete themselves after completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set short-lived reminders, checks, or one-time scheduled actions without adding permanent HEARTBEAT.md entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores free-form task text for later execution without clear safety boundaries or auditability.

Mitigation: Use it only for inert reminders or tightly approved actions, and require the host agent to recheck permission before executing any task that modifies files, accesses private data, calls external services, or affects business workflows.

Risk: Task files are designed to be deleted after execution.

Mitigation: Install only where automatic deletion of completed temporary task files is acceptable, and retain separate audit records when task history is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/skills/temp-heartbeat)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown task summaries, tables, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write temporary task files under memory/ and delete them after execution.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
