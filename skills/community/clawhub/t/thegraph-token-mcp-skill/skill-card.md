## Description: <br>
Use The Graph Token API MCP through UXC for token metadata, wallet balances, transfers, holders, pools, and market data with help-first inspection and Token API specific JWT bearer auth binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect and query The Graph Token API MCP for token metadata, wallet balances, transfers, holders, pools, and market data. It guides setup of a dedicated Token API JWT credential and encourages narrow, help-first API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A compromised or untrusted local UXC tool could affect command execution or credential handling. <br>
Mitigation: Verify that the local `uxc` installation is trusted before using the skill. <br>
Risk: Reusing another The Graph credential or storing the wrong token type can cause authentication failures or unintended credential exposure. <br>
Mitigation: Use a dedicated The Graph Token API JWT from the The Graph Market dashboard and keep it separate from other The Graph credentials. <br>
Risk: Wallet addresses, token contracts, and queried assets are sent to The Graph's API. <br>
Mitigation: Query only addresses and assets that the user is comfortable sharing with the API provider, and start with narrow requests. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [The Graph Token API MCP endpoint](https://token-api.mcp.thegraph.com/) <br>
- [The Graph Market dashboard](https://thegraph.market/dashboard) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/thegraph-token-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses help-first MCP inspection and expects JSON response envelopes from UXC.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
