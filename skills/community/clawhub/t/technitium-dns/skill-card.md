## Description:

Monitor and inspect Technitium DNS Server via its HTTP API for read-only health checks, DNS stats, zones, DHCP leases, token/session validation, and proactive DNS/DHCP alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naamah75](https://clawhub.ai/user/naamah75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor a Technitium DNS Server instance, validate API/session access, inspect DNS and DHCP health signals, and summarize actionable failures without changing server configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A sensitive Technitium API/session token can be exposed if sent over plaintext HTTP or through redirects.

Mitigation: Use an HTTPS endpoint you control, avoid non-loopback HTTP examples, and rotate any token that may have crossed plaintext transport.

Risk: The health check requires a token that can access DNS and DHCP monitoring endpoints.

Mitigation: Use a dedicated least-privilege Technitium user or token for monitoring and avoid granting write privileges.

Risk: Automated monitoring can create unnecessary API load if run too frequently.

Mitigation: Run checks only on a planned heartbeat interval and stay silent when the JSON result reports ok as true.

## Reference(s):

- [Technitium DNS Server project](https://github.com/TechnitiumSoftware/DnsServer)
- [Technitium DNS Server API documentation](https://github.com/TechnitiumSoftware/DnsServer/blob/master/APIDOCS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON health-check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper prints JSON with ok, checked, and failures fields and exits with status codes for healthy, critical-failure, and configuration/session-failure outcomes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
