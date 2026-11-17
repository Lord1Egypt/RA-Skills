## Description:

Queries Sato Hub for onchain-agent tooling, adoption measurements, install checks, and preflight or routing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satohubai](https://clawhub.ai/user/satohubai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can compare onchain-agent components, investigate published adoption figures, check packages and endpoints before installation, and review proposed routes before signing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries sent to Sato Hub may reveal repository names, endpoint URLs, token addresses, route parameters, or secrets included in submitted configurations.

Mitigation: Scrub secrets, private keys, bearer tokens, and sensitive MCP configuration before sending a query; share only information you intend to disclose.

Risk: Scores and preflight verdicts may be mistaken for security assurances, while route quotes and fees can change before a transaction is signed.

Mitigation: Treat checks as evidence rather than audits; verify current venue facts, fees, and transaction details independently before signing.

## Reference(s):

- [Sato Hub MCP documentation](https://satohub.ai/mcp)
- [Sato Hub MCP endpoint](https://satohub.ai/api/mcp)
- [ClawHub skill release](https://clawhub.ai/satohubai/skills/sato-hub)
- [MCP tool reference](references/tools.md)
- [REST API reference](references/rest.md)
- [Worked examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links and dated evidence where available.]

## Skill Version(s):

1.2.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
