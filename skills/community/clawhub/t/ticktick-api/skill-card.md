## Description:

TickTick API helps agents manage TickTick projects and tasks by listing projects and tasks, creating tasks, completing tasks, and deleting tasks after OAuth setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiofreitas](https://clawhub.ai/user/kaiofreitas)

### License/Terms of Use:


## Use Case:

External users and productivity-focused teams use this skill to manage TickTick to-do lists from an agent, including checking pending work, adding reminders or due dates, and marking tasks done.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets can be exposed when passed directly on the command line.

Mitigation: Use secure secret handling where available, avoid shell history exposure, and rotate or revoke any client secret that may have been exposed.

Risk: The skill relies on unspecified `ticktick` and `ticktick-setup` command implementations.

Mitigation: Install only trusted command implementations and verify OAuth token storage and revocation behavior before authorizing an account.

Risk: Complete and delete operations can change or remove TickTick task data.

Mitigation: Confirm state-changing and destructive task operations explicitly before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiofreitas/skills/ticktick-api)
- [TickTick Developer Portal](https://developer.ticktick.com)
- [TickTick Open API](https://api.ticktick.com/open/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce instructions that call external TickTick command-line tools and modify TickTick task data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
