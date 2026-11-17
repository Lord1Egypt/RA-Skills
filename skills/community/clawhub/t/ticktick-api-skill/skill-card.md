## Description:

Helps agents manage TickTick tasks and projects through a user-authorized Maton connection, with optional scheduled or cross-app automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using an agent to list, create, update, complete, and organize TickTick tasks and projects can use this skill to work through their authorized account. Developers can also set up approved functions and triggers for recurring or cross-app actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting TickTick grants the integration access to tasks and projects in the authorized account.

Mitigation: Confirm the intended account and connection with the user and grant only the access needed for the task.

Risk: Writes, hosted functions, and triggers can alter tasks or run actions automatically.

Mitigation: Review the exact action and target with the user before approving writes or automation.

Risk: Persistent trigger destinations can forward matching event data to a configured URL.

Mitigation: Approve destinations separately after reviewing the destination URL, data flow, and connected account.

## Reference(s):

- [TickTick skill on ClawHub](https://clawhub.ai/byungkyu/skills/ticktick-api-skill)
- [Maton](https://maton.ai)
- [Maton API documentation](https://docs.maton.ai/api-reference/overview)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [TickTick Developer Portal](https://developer.ticktick.com/)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task and project actions require an authorized connection; writes and new connections require user confirmation.]

## Skill Version(s):

1.2.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
