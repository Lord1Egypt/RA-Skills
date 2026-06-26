## Description: <br>
Query TRON real-time network data including latest block height, current TPS, node count, latest TVL, total transaction count, and real-time vote count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill through the TronScan MCP service to answer current TRON network status questions such as TPS, block height, node count, TVL, transaction totals, and witness vote counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the TronScan service without an API key can encounter API rate limits or 429 errors. <br>
Mitigation: Configure a dedicated TronScan API key only in the intended MCP configuration when higher call volume is needed. <br>
Risk: Latest solidified block data can lag the chain head, and some block detail fields may be null or zero. <br>
Mitigation: Clarify solidified-block semantics in responses and use a block-detail skill when users need fields not returned by this realtime endpoint. <br>


## Reference(s): <br>
- [TronScan MCP Server](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/sshnii/tronscan-realtime-network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Markdown or plain text summaries backed by MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public network statistics; an optional dedicated TronScan API key may be configured for rate limits.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
