## Description:

Query TRON latest block, block reward, block time, producer, burned TRX, resource use, and transaction count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for TRON block data such as current block height, producer, reward context, burned TRX, resource use, and transaction counts through the TronScan MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to the TronScan MCP server to query public TRON block data.

Mitigation: Confirm the user is comfortable using the TronScan MCP server before installing or enabling the skill.

Risk: Using a TronScan API key may increase request limits but adds credential-handling responsibility.

Mitigation: Add a TronScan API key to MCP configuration only when intentionally needed, and manage it as a secret.

Risk: Some latest-block fields may be returned as null or 0 by the underlying TronScan endpoint.

Mitigation: Use the block-list tool for witness names, reward, fee, and resource-usage details when latest-block responses omit them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-block-info)
- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown or plain text summaries of TronScan MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include block numbers, hashes, timestamps, witness or producer data, transaction counts, burn totals, and rate-limit troubleshooting guidance.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
