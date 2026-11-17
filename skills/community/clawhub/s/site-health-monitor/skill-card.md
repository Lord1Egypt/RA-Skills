## Description:

Monitor websites for uptime, SSL certificate expiry, response time, HTTP errors, and content changes, then generate health reports and alerts when issues are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and external teams use this skill to run one-off or scheduled checks for website uptime, SSL expiry, response time, HTTP status, and planned content-change monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make network requests from the agent host to user-provided targets.

Mitigation: Avoid checking localhost, private network names or IPs, cloud metadata addresses, or other sensitive internal targets.

Risk: The SSL check can give false assurance about certificate trust or hostname matching.

Mitigation: Do not treat the SSL status as proof that a certificate is trusted or matches the hostname until validation is fixed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/charlie-morrison/skills/site-health-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health reports with JSON script outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may summarize single-site or multi-site status, alerts, SSL expiry, response timing, and HTTP errors.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
