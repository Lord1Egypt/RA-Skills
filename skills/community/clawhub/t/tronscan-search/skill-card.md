## Description:

Search TRON blockchain data by name or keyword to resolve token or contract names to addresses and find accounts, transactions, or blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search public TRON blockchain data through TronScan MCP when they need to resolve a token or contract name, inspect an account, or look up a transaction or block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references adding a TronScan API key for rate limits but does not define credential storage.

Mitigation: Review TronScan MCP setup separately and store any API key only in approved MCP settings or secret-management paths.

Risk: Search results can include a tokenCanShow false signal.

Mitigation: Warn the user before proceeding when tokenCanShow is false and use the token scanner skill for detailed risk-field semantics.

Risk: Name or keyword searches can return ambiguous TRON blockchain matches.

Mitigation: Use the optional type filter and verify returned token, contract, account, transaction, or block identifiers before acting on them.

## Reference(s):

- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan Developer API](https://tronscan.org/#/developer/api)
- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-search)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance for TronScan MCP search calls and result interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search guidance covers the required term parameter plus optional type, start, and limit filters.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
