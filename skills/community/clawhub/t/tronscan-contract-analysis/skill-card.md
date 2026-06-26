## Description: <br>
Analyze TRON contracts for deploy information, hot methods, top callers, open-source verification status, and transaction count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and TRON ecosystem analysts use this skill to inspect contract metadata, verification status, call patterns, events, energy usage, and caller activity through the TronScan MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TRON contract or address queries are sent to the disclosed TronScan MCP service. <br>
Mitigation: Use the skill only when sharing those query details with TronScan is acceptable. <br>
Risk: Routing ambiguity can occur for token-holder, token-supply, or account-balance questions. <br>
Mitigation: Use the more specific token or account skills for token-holder, token-supply, and account-balance requests. <br>
Risk: Contract verification status reflects source-code availability and verification on TronScan, not official endorsement or project certification. <br>
Mitigation: Treat verification as a code-level signal and combine it with call statistics, events, energy usage, and other review evidence before making safety conclusions. <br>
Risk: TronScan API rate limits may affect analysis completeness. <br>
Mitigation: If rate limits occur, configure a TronScan developer API key and retry with appropriate pagination or time ranges. <br>


## Reference(s): <br>
- [TronScan Contract Analysis on ClawHub](https://clawhub.ai/sshnii/tronscan-contract-analysis) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan MCP Server](https://mcp.tronscan.org/mcp) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or plain-text analysis with TronScan MCP tool call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only contract analysis; outputs may include contract metadata, verification status, call statistics, event summaries, energy usage, transaction counts, caller lists, and routing guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
