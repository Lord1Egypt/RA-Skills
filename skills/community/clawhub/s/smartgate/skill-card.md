## Description:

Connect OpenClaw to SmartGate’s hosted MCP tools for search, fetching, text processing, context and budget management, memory, and pipelines; it requires SMARTGATE_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smartgate.network](https://clawhub.ai/user/smartgate.network)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers configure SmartGate’s hosted MCP service to search and fetch web content, process text, manage context and token budgets, store or recall team facts, and run tool pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposure of the SmartGate API key could allow unauthorized use of the account.

Mitigation: Keep the key out of chat and repositories; provide it through the SMARTGATE_API_KEY environment variable.

Risk: Private text or team facts sent to the hosted service may be subject to its data-retention terms.

Mitigation: Review SmartGate’s pricing and data-retention terms before sending private text or storing team facts.

## Reference(s):

- [SmartGate tools documentation](https://smartgate.network/docs/tools)
- [SmartGate](https://smartgate.network)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration instructions, Shell commands]

**Output Format:** [Hosted MCP tool responses; Markdown setup guidance with shell and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured hosted MCP connection and SMARTGATE_API_KEY.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
