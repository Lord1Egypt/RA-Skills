## Description:

Doctorbot Healthcheck Free performs a free, read-only OpenClaw security and health audit to detect security risks, outdated software, and misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bamontejano](https://clawhub.ai/user/bamontejano)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to ask an agent to inspect an OpenClaw host's security posture, update status, firewall and open-port state, OS version, and running services, then summarize results as a health report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health-check report may expose sensitive host security details such as open ports, firewall state, OS details, and running services.

Mitigation: Treat the report as sensitive system information, restrict sharing, and redact host-specific details before posting or attaching it.

Risk: The skill asks the agent to inspect local OpenClaw and system security state.

Mitigation: Review proposed commands before execution and run the skill only in environments where local security inspection is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bamontejano/skills/skill-doctorbot-healthcheck-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with health-check findings and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only inspection output may contain sensitive host security details.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
