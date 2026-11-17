## Description:

Analyze DMARC reports and SPF/DKIM issues, inspect domains and original report XML, and onboard MSP clients in your Suped account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suped](https://clawhub.ai/user/suped)

### License/Terms of Use:

MIT-0

## Use Case:

Suped account holders use this skill to review DMARC reports, investigate SPF/DKIM issues, inspect saved issues and original report XML, and add domains or MSP clients when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection can read accessible Suped reports and create domains or MSP clients, so an unintended target or shared operator login can expose data or make unwanted changes.

Mitigation: Connect an appropriately limited account, confirm the intended organization before creation, and avoid sharing the operator connection with untrusted users.

## Reference(s):

- [Suped MCP documentation](https://www.suped.com/docs/mcp)
- [OpenClaw MCP OAuth documentation](https://docs.openclaw.ai/cli/mcp/transports)
- [Suped DMARC on ClawHub](https://clawhub.ai/suped/skills/suped-dmarc)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, API calls, Shell commands, Configuration]

**Output Format:** [Markdown text, with shell commands or configuration examples when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are tailored to the selected organization, domain, and date range, and may summarize Suped records or original report XML.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
