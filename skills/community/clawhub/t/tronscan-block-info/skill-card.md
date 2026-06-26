## Description: <br>
Query TRON latest block, block reward, block time, producer, burned TRX, resource use, and transaction count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to answer TRON block questions such as latest block height, producer, block reward context, burned TRX, resource use, and transaction counts through TronScan MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TRON block lookup requests are sent to TronScan's MCP service. <br>
Mitigation: Install only if sending public block lookup requests to TronScan is acceptable for the intended use case. <br>
Risk: Unauthenticated TronScan API usage may encounter rate limits. <br>
Mitigation: Configure a TronScan API key only when higher rate limits are needed, and manage that key outside the skill content. <br>


## Reference(s): <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan MCP Server](https://mcp.tronscan.org/mcp) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/sshnii/tronscan-block-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with MCP tool call recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only TRON block information queries via the disclosed TronScan MCP service.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata; skill frontmatter metadata version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
