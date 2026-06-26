## Description: <br>
Queries TRON transaction results, confirmation status, sender and receiver details, token transfers, internal transactions, resource consumption, and transaction statistics through the TronScan MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to investigate TRON transaction hashes, explain success or failure, confirm transaction status, identify senders and receivers, inspect token movements, and understand energy or bandwidth consumption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public TRON transaction hashes and related addresses are sent to the disclosed TronScan MCP service. <br>
Mitigation: Use only public transaction identifiers and addresses, and avoid entering private keys, seed phrases, or other secrets. <br>
Risk: Unauthenticated use may hit TronScan rate limits. <br>
Mitigation: Configure a TronScan API key in MCP settings only when higher rate limits are needed. <br>
Risk: Some token fields can indicate a potentially risky token involved in a transaction. <br>
Mitigation: Warn users when transaction token entries include tokenCanShow false or tokenLevel values of 3 or 4. <br>


## Reference(s): <br>
- [TronScan MCP service endpoint](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>
- [ClawHub skill page](https://clawhub.ai/sshnii/tronscan-transaction-info) <br>
- [Publisher profile](https://clawhub.ai/user/sshnii) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with TronScan MCP lookup results and transaction interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include unit conversions for sun-to-TRX values and risk warnings for token fields such as tokenCanShow or tokenLevel.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
