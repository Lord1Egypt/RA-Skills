## Description:

Query Renzo crypto liquid restaking protocol data, including DeFi vault yields, TVL, ezETH exchange rates, EigenLayer operators, supported networks, user token balances, and withdrawal status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pooleja](https://clawhub.ai/user/pooleja)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve live Renzo liquid restaking metrics, compare vaults and operators, and check address-specific balances or withdrawal status when an Ethereum address is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-specific balance and withdrawal queries send the provided Ethereum address to Renzo Protocol's MCP server.

Mitigation: Use those queries only when the user supplies an Ethereum address and is comfortable sharing it with Renzo Protocol.

Risk: Live APR, TVL, balance, and withdrawal data can be unavailable or change after retrieval.

Mitigation: Present results as current at query time and report endpoint failures in plain language.

## Reference(s):

- [ClawHub Renzo skill page](https://clawhub.ai/pooleja/skills/renzo)
- [Renzo MCP endpoint](https://mcp.renzoprotocol.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summaries with tables, plus JSON returned by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; address-specific balance and withdrawal queries send the provided Ethereum address to Renzo Protocol's MCP server.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
