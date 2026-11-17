## Description:

Record, search, summarize, and export local IoT sensor-related entries from a terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, field operators, and support teams can use this skill to keep local timestamped notes about sensor readings, device status, telemetry observations, configurations, reports, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the skill for real IoT polling, connectivity checking, conversion, or telemetry analysis.

Mitigation: Treat it as a local sensor note logger and verify device state, conversions, and analysis with dedicated IoT tooling before relying on results.

Risk: Sensor notes, hostnames, credentials, or incident details entered into commands may be persisted in durable local files.

Mitigation: Avoid entering secrets or sensitive operational details unless local persistence under the configured data directory is acceptable.

## Reference(s):

- [Sensor ClawHub skill page](https://clawhub.ai/ckchzh/skills/sensor)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown guidance with shell command examples; the installed script also writes local JSON, CSV, and text exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local terminal responses and files under the configured sensor data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
