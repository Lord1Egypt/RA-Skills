## Description:

Turn a role or ICP spec into a ranked outbound sales list of LinkedIn prospects enriched with company context and one-line opener rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

External sales and go-to-market users use this skill to convert an ideal customer profile or role description into a ranked LinkedIn prospect list with company context and grounded opener rationale. It is intended for prospect discovery and outreach preparation, not contact-detail extraction or message sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prospecting criteria and LinkedIn lookup requests are sent to Veezee APIs.

Mitigation: Confirm the user is comfortable sharing those inputs with Veezee and avoid sending unnecessary sensitive data.

Risk: The Veezee API key is a credential that may be stored by the host, SDK, or CLI.

Mitigation: Use MCP authorization or secure secret storage where available, and treat the key like any other bearer credential.

Risk: Running an unpinned npx command can execute the latest published SDK package.

Mitigation: Prefer MCP authorization or a pinned and reviewed SDK version before use.

Risk: The skill can prepare prospecting lists but cannot provide contact details or send outreach.

Mitigation: Tell users plainly that outputs are LinkedIn-based prospect summaries and opener rationale, not email, phone, or automated outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezee-build/skills/veezee-outreach-list-builder)
- [Veezee LinkedIn MCP endpoint](https://mcp.veezee.io/linkedin)
- [Veezee all-tools MCP endpoint](https://mcp.veezee.io/all)
- [Veezee API key mint endpoint](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown ranked list with per-prospect company notes, opener rationale, skipped-private count, and total credits spent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses LinkedIn profile and company data only; does not produce email addresses, phone numbers, or sent outreach.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
