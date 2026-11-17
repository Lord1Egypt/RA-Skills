## Description:

Query TRON real-time network data including latest block height, current TPS, node count, latest TVL, total transaction count, and real-time vote count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to answer current TRON network-status questions through TronScan MCP tools, including TPS, block height, node count, TVL, total transaction count, and witness vote totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TRON network-stat questions are routed through the TronScan MCP service.

Mitigation: Install only when use of the TronScan MCP service is acceptable for the intended workflow.

Risk: Rate-limit credentials may be needed for higher TronScan API usage.

Mitigation: Configure any API key only through MCP settings and avoid sharing credentials in chat.

Risk: Some block-detail fields may be unavailable or returned as zero or null by the underlying API.

Mitigation: Treat unavailable fields as absent and use a block-detail skill when detailed block fields are required.

## Reference(s):

- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)
- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-realtime-network)
- [Publisher Profile](https://clawhub.ai/user/sshnii)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text responses based on live TronScan MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current network metrics returned by the configured TronScan MCP service.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
