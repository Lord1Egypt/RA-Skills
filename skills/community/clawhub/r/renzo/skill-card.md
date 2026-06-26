## Description: <br>
Query Renzo crypto liquid restaking protocol data, including DeFi vault yields, TVL, ezETH exchange rates, EigenLayer operators, supported blockchain networks, user token balances, and withdrawal status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pooleja](https://clawhub.ai/user/pooleja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to query live Renzo Protocol data, compare vault yields and TVL, inspect supported chains and operators, and check address-specific Renzo token balances or withdrawal status when an Ethereum address is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-specific balance and withdrawal checks send the provided Ethereum address to the Renzo MCP server. <br>
Mitigation: Use these tools only when comfortable sharing that address with Renzo; do not provide private keys, seed phrases, or unrelated personal data. <br>
Risk: Responses depend on the availability and accuracy of the external Renzo MCP server. <br>
Mitigation: Treat returned APR, TVL, balance, and withdrawal data as live external data and retry later or verify through Renzo if the server is unreachable or results look unexpected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pooleja/renzo) <br>
- [Renzo MCP Server](https://mcp.renzoprotocol.com/mcp) <br>
- [Skill Homepage](https://github.com/Renzo-Protocol/openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON tool results summarized as readable text or tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; calls the public Renzo MCP endpoint and returns read-only protocol data.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
