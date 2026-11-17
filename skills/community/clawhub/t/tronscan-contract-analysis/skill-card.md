## Description:

Analyze TRON contracts for deployment information, call statistics, callers, events, energy usage, open-source verification status, and transaction activity using TronScan MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect public TRON contract details, verification status, call activity, top callers, events, energy consumption, and transaction trends. It supports contract-analysis workflows but is not a replacement for a smart-contract audit or token/project safety review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat TronScan contract verification or open-source status as proof that a token or project is endorsed, certified, or safe.

Mitigation: State that verification only means the contract source code has been open-sourced and verified on TronScan, and recommend independent review before relying on the contract.

Risk: Broad TRON contract, token-holder, or account-balance questions may be routed outside the skill's intended contract-analysis scope.

Mitigation: Confirm that the request is about contract analysis and redirect token supply, holder-list, or address-balance requests to the appropriate specialized workflow.

Risk: TronScan MCP connection issues or API rate limits can interrupt public data lookups.

Mitigation: Surface connection or rate-limit errors clearly and advise configuring TronScan MCP or API access before retrying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sshnii/skills/tronscan-contract-analysis)
- [TronScan MCP server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text analysis based on TronScan MCP results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public contract details, verification status, call statistics, caller summaries, events, energy usage, and transaction activity.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
