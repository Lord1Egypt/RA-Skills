## Description:

Monitor uptime of websites/services and alert when down.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check whether websites or services are reachable, send downtime alerts, and generate uptime summaries from local logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound HTTP requests to arbitrary monitored URLs.

Mitigation: Restrict MONITOR_URLS to approved public HTTPS endpoints and avoid internal hostnames or URLs containing secrets.

Risk: Alert delivery can send service details to an external webhook or email destination.

Mitigation: Set ALERT_WEBHOOK_URL and ALERT_EMAIL only to approved destinations and review alert content before deployment.

Risk: Logs and generated reports may contain untrusted or sensitive service information.

Mitigation: Treat generated logs and reports as untrusted when monitored URLs can be influenced by others, and avoid including secrets in URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/service-health-checker)
- [Publisher profile](https://clawhub.ai/user/kryzl19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health-check output uses pipe-delimited status lines; reports are Markdown summaries generated from local logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
