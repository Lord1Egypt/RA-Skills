## Description:

Work with your own Recued server from OpenClaw. Read your notes, tasks and the things you own, and propose changes that wait for your approval in Recued.

This skill is ready for commercial/non-commercial use.

## Publisher:

[recued](https://clawhub.ai/user/recued)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users with a Recued server use this skill to read their notes, tasks, mail, calendar, and owned items, and to propose changes that require their approval in Recued.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A contract that grants more access than needed could expose personal records or permit unwanted actions.

Mitigation: Grant only the tools needed and keep change approvals enabled in Recued.

Risk: Someone with access to the contract token could use the permissions it grants.

Mitigation: Protect RECUED_MCP_TOKEN and keep it in the gateway environment file rather than embedding the key in configuration.

Risk: Personal records returned by Recued may be visible to the model used by OpenClaw.

Mitigation: Review which records your chosen model may receive.

## Reference(s):

- [Recued](https://recued.com)
- [Install the Recued server](https://recued.com/docs/setup/install-server/)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
