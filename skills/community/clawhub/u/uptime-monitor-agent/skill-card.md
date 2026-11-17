## Description:

Monitor uptime of websites/services and alert when down.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check whether HTTP endpoints are reachable, send downtime alerts, and generate uptime summaries from local logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTP requests to monitored URLs and an optional alert webhook, with minimal URL validation.

Mitigation: Configure MONITOR_URLS and ALERT_WEBHOOK_URL only with destinations you trust, and avoid attacker-supplied URLs.

Risk: Webhook alerts may expose monitored URLs, status codes, response times, and error details to the configured destination.

Mitigation: Treat webhook URLs as sensitive secrets and send alerts only to approved notification endpoints.

Risk: The scripts write local status and alert logs that may contain service URLs and operational details.

Mitigation: Store logs in an appropriate workspace location and review retention or access controls before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kryzl19/skills/uptime-monitor-agent)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kryzl19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces HTTP status check output, alert guidance, and uptime report summaries; requires curl for HTTP checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
