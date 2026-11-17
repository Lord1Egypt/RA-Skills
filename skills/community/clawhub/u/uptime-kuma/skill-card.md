## Description:

Interact with Uptime Kuma monitoring server to check monitor status, add or remove monitors, pause or resume checks, and view heartbeat history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msarheed](https://clawhub.ai/user/msarheed)

### License/Terms of Use:


## Use Case:

Developers, operators, and site reliability teams use this skill to administer Uptime Kuma monitors and inspect service health from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete monitors or pause monitoring, including workflows that pause all monitors.

Mitigation: Require explicit human confirmation before delete operations or any pause-all maintenance workflow.

Risk: The skill administers an Uptime Kuma instance using supplied credentials.

Mitigation: Use a dedicated least-privileged Uptime Kuma account and install dependencies in an isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/msarheed/skills/uptime-kuma)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text or JSON, often accompanied by Markdown shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Uptime Kuma connection settings and credentials in environment variables.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
