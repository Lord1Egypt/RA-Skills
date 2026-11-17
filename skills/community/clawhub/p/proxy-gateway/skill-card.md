## Description:

Secure HTTP proxy access for AI agents that need web scraping, API integrations, data collection, or research automation through hosted or self-hosted proxy gateway workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kehongpeng](https://clawhub.ai/user/kehongpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to route agent HTTP requests through a proxy service or deploy their own gateway for public web access, scraping, API calls, and data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy operators can see request URLs, headers, bodies, and responses.

Mitigation: Use the skill only for public, non-sensitive data; do not send secrets or sensitive data through hosted proxy paths; self-host when privacy is required.

Risk: Network forwarding can create high-impact exposure if deployed without tight scoping.

Mitigation: For self-hosting, isolate the deployment and apply egress filtering that blocks loopback, private networks, metadata services, unsafe redirects, and unnecessary methods or headers.

Risk: Payment and account endpoints require review before production use.

Mitigation: Review mainnet USDC deposits, balance and history access, free-trial abuse controls, Redis security, and dependency update practices before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kehongpeng/skills/proxy-gateway)
- [Proxy Gateway Service Documentation](https://proxy.easky.cn)
- [Security Policy](SECURITY.md)
- [x402 Integration Guide](docs/X402_INTEGRATION.md)
- [Polygon Network](https://polygon.technology)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hosted-service API usage, self-hosting steps, proxy configuration, and payment-related setup guidance.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
