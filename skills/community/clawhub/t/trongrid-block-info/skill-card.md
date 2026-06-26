## Description: <br>
Query and analyze TRON blocks including producer info, transaction breakdown, rewards, burns, and network load. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, blockchain analysts, and operations teams use this skill to inspect TRON block details, producer information, transaction activity, resource consumption, and block economics through a TronGrid MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external TronGrid MCP server, so actual network behavior and access controls are determined outside the skill instructions. <br>
Mitigation: Review the MCP server configuration before use and install only when public TRON blockchain analysis is intended. <br>
Risk: Block rewards, burns, fees, and producer attribution can be misleading if stale, incomplete, or unconfirmed block data is returned. <br>
Mitigation: Use the latest confirmed block path when finality matters and report uncertainty when data is missing or a block has no events. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown block reports with MCP tool-call guidance and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only analysis of public TRON block data; live results depend on the configured TronGrid MCP server.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
