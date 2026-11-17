## Description:

Provides SmartPi IoT device-control guidance for lights, humidifiers, curtains, and device status queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namishisu](https://clawhub.ai/user/namishisu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure SmartPi credentials and generate curl-based commands for controlling and querying supported IoT devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands may immediately control real SmartPi devices.

Mitigation: Require explicit confirmation before running commands that turn devices on, change brightness, or open curtains.

Risk: Credentials can be exposed through logs, shell history, or copied command examples.

Mitigation: Use scoped credentials where possible and keep SMARTPI_TOKEN and device identifiers out of logs, history, and version control.

Risk: The skill depends on a live SmartPi endpoint that must be trusted before use.

Mitigation: Install only after confirming trust in the SmartPi endpoint and validating network access to mcp.aimachip.com.

## Reference(s):

- [SmartPi official website](https://smartpi.cn/)
- [SmartPi API base endpoint](https://mcp.aimachip.com)
- [ClawHub skill page](https://clawhub.ai/namishisu/skills/smartpi-iot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus SMARTPI_TOKEN and SMARTPI_DEVICE_KEY environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
