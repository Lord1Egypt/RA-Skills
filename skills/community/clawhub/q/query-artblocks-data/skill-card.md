## Description:

Query Art Blocks on-chain data using artblocks-mcp GraphQL tools for projects, tokens, artists, sales, traits, and custom data needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryley-o](https://clawhub.ai/user/ryley-o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to guide Art Blocks data retrieval through domain-specific MCP tools or custom GraphQL queries when they need project, token, artist, sales, traits, wallet, or multi-chain on-chain data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw GraphQL queries can return broad public Art Blocks blockchain datasets, including wallet, token ownership, and sales records.

Mitigation: Use specific filters, limits, chain IDs, and domain-specific tools when they cover the request.

Risk: Custom schema exploration and joins can produce invalid or inefficient queries when fields or tables are assumed.

Mitigation: Use explore_table, validate_fields, build_query, and query_optimizer before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryley-o/skills/query-artblocks-data)

## Skill Output:

**Output Type(s):** [guidance, code, API calls]

**Output Format:** [Markdown guidance with GraphQL code blocks and tool-call recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public Art Blocks wallet, token ownership, sales, and chain-specific query results returned through MCP GraphQL tools.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
