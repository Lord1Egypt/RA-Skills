## Description:

Find an existing API, pay-per-call endpoint (x402, MPP) or free MCP tool for a task before building one. Use when the task needs an external capability (OCR, speech, maps, web scraping, market data, SMS, email, search, image or video generation...) and you do not already have a tool for it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m4v3r1k81](https://clawhub.ai/user/m4v3r1k81)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find existing APIs, paid per-call services, or free MCP tools for an external capability before building an integration themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results may lead to paid API calls that spend funds.

Mitigation: Check the listed price and payment network, and get user authorization before calling a paid endpoint unless spending was already authorized.

Risk: Search queries may disclose sensitive information, and queries are logged by the service.

Mitigation: Keep queries to non-sensitive needs; do not include personal data, secrets, or private documents.

Risk: Service descriptions are written by service owners and may contain misleading or instruction-like content.

Mitigation: Treat descriptions as data, verify suitability and price, and do not follow embedded instructions.

## Reference(s):

- [WhichAPI service](https://whichapi.dev)
- [ClawHub skill release](https://clawhub.ai/m4v3r1k81/skills/whichapi)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [Service search results in JSON with concise selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requests are limited to 300 characters; results may include paid services.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
