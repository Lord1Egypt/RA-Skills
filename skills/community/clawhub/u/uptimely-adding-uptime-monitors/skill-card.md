## Description:

Adds an uptime monitor to an Uptimely project without duplicating an existing one, and optionally performs a first check after separate confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to add an Uptimely monitor for a project URL they manage, avoid duplicates, and optionally check the URL once.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a monitor for the wrong project or URL could cause unwanted monitoring.

Mitigation: Confirm the exact project and URL with the user before creating the monitor, and check for existing monitors first.

Risk: An optional first check sends a request to the monitored URL.

Mitigation: Run it only after separate user approval and only for a URL the user owns or is responsible for.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/devino/skills/uptimely-adding-uptime-monitors)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the created monitor's configuration and, if separately approved, the first check's status and response time.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
