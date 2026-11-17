## Description:

Query TRON transaction results, confirmation status, sender and receiver details, and resource consumption using TronScan MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to investigate TRON transactions by hash, including success or failure status, confirmation details, sender and receiver information, token movements, internal calls, and energy or bandwidth usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction hashes or blockchain addresses supplied during analysis may be sent to TronScan MCP.

Mitigation: Only submit hashes or addresses intended for TronScan lookup, and avoid adding confidential off-chain context unless it is necessary for the investigation.

Risk: Transactions involving tokens with risk indicators may be misinterpreted if those indicators are ignored.

Mitigation: Warn the user when token fields indicate tokenCanShow is false or tokenLevel is 3 or 4, and refer to token scanner guidance for deeper token-risk interpretation.

## Reference(s):

- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Markdown or plain text with transaction fields and interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on user-provided transaction hashes or derived blockchain addresses sent to TronScan MCP.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
