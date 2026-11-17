## Description:

Guides an agent to query TRON Super Representatives, witnesses, candidates, voting information, chain parameters, and governance proposals through TronScan MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and TRON users use this skill to guide agents through TronScan MCP lookups for SR rankings, account voting records, chain configuration, proposal lists, witness vote metrics, and network vote summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may include public TRON blockchain addresses.

Mitigation: Avoid submitting private or sensitive address context that is not needed for the governance lookup.

Risk: TronScan MCP or API requests may be rate-limited when no API key is configured.

Mitigation: Configure a TronScan API key in the MCP setup when rate limits affect expected usage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-sr-governance)
- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan Developer API](https://tronscan.org/#/developer/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown guidance with TronScan MCP tool names, query inputs, and response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve public TRON blockchain addresses; TronScan API key configuration may be needed if rate limits are encountered.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
