## Description:

Monitor uptime of websites and services and alert when they go down.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to check HTTP endpoints, receive webhook or email alerts when services are unreachable, and generate markdown uptime reports from local logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTP requests to monitored URLs and optional alert destinations.

Mitigation: Monitor only trusted URLs and configure webhook or email destinations that the user controls.

Risk: Alert payloads can disclose service URLs, status codes, response times, and error details to external systems.

Mitigation: Avoid sensitive internal endpoints unless external alerting is intentional and approved.

Risk: Generated logs and uptime reports are operational records, not tamper-resistant audit evidence.

Mitigation: Use the reports for monitoring visibility and keep separate audit controls where integrity guarantees are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/strd-uptime-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Shell command output and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; checks and alert scripts write local operational logs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
