## Description:

Use The Graph Token API MCP through UXC for token metadata, wallet balances, transfers, holders, pools, and market data with help-first inspection and Token API specific JWT bearer auth binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure UXC access to The Graph Token API MCP and query token metadata, wallet balances, transfers, holders, pools, and market data with operation-level help before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A The Graph Token API JWT could be confused with another The Graph credential or reused in the wrong binding.

Mitigation: Store the Token API JWT separately, bind it only to token-api.mcp.thegraph.com, and verify the active UXC credential binding before use.

Risk: Token and wallet queries are sent to The Graph's MCP endpoint.

Mitigation: Review the intended query data before execution, start with narrow token or wallet requests, and remove or rotate the UXC binding when access is no longer needed.

Risk: Endpoint operation names or argument shapes may change over time.

Mitigation: Inspect host and operation help before execution and parse stable JSON envelope fields such as ok, kind, protocol, data, and error.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [The Graph Token API MCP endpoint](https://token-api.mcp.thegraph.com/)
- [The Graph Market dashboard](https://thegraph.market/dashboard)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/thegraph-token-mcp-skill)
- [jolestar publisher profile](https://clawhub.ai/user/jolestar)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP operation names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance favors JSON envelope parsing and narrow read queries before broader scans.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
