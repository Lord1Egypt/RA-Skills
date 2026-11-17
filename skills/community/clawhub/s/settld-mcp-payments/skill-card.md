## Description:

Connect OpenClaw agents to Settld MCP for paid tool calls with quote-bound authorization and verifiable receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidenlippert](https://clawhub.ai/user/aidenlippert)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure OpenClaw agents for Settld paid MCP tools, including quote-bound authorization, payment retry flow, and receipt-producing responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server setup runs an unpinned npm package for paid tool access.

Mitigation: Pin an exact reviewed package version and install through a controlled process with a lockfile or integrity checks before enabling the server.

Risk: The skill requires Settld credentials and can enable paid tool calls.

Mitigation: Use narrowly scoped, revocable API keys and enforce tenant policy, provider allowlists, and spend limits before use.

Risk: Payment and settlement outputs may include sensitive operational headers or receipt data.

Mitigation: Avoid exposing secrets in chat output and share only the receipt or settlement headers required for audit.

## Reference(s):

- [Settld MCP Payments skill page](https://clawhub.ai/aidenlippert/skills/settld-mcp-payments)
- [Publisher profile: aidenlippert](https://clawhub.ai/user/aidenlippert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Settld MCP tool names, environment variable guidance, and payment or settlement header handling.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
