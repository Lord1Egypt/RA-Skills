## Description: <br>
Query TRON Super Representatives, witnesses, candidates, voting information, chain parameters, and governance proposals through TronScan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and TRON ecosystem operators use this skill to look up Super Representative rankings, account votes, chain parameters, governance proposals, and witness vote metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Governance queries and TRON addresses entered by the user are sent to the disclosed TronScan MCP service. <br>
Mitigation: Use the skill only when sharing those query details with TronScan is acceptable. <br>
Risk: Optional TronScan API keys used for rate limits could be exposed if stored or shared carelessly. <br>
Mitigation: Store API keys in the agent or MCP configuration secret mechanism and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sshnii/tronscan-sr-governance) <br>
- [TronScan MCP endpoint](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown or text guidance with structured MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only TronScan governance lookups; optional API key configuration may be used for rate limits.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
