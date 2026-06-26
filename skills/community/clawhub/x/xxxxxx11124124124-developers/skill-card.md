## Description: <br>
Longbridge platform expert for investment analysis and developer tasks across market analysis, portfolio queries, Longbridge CLI usage, Python and Rust SDK development, MCP setup, and LLM/RAG documentation integration for HK, US, CN, SG, and Crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huacnlee](https://clawhub.ai/user/huacnlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and engineers use this skill to retrieve Longbridge market data, analyze securities and portfolios, configure Longbridge MCP access, and write Longbridge CLI or SDK workflows. It supports investment research and brokerage-related automation, including quote, news, filing, position, and order-oriented tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward sensitive portfolio access and brokerage actions. <br>
Mitigation: Use read-only scopes where possible and require explicit user confirmation before any account or trade action. <br>
Risk: Installation examples may involve remote scripts or live order examples. <br>
Mitigation: Inspect remote install scripts before execution and avoid running live order examples unchanged. <br>
Risk: OAuth authorizations may persist after the immediate task is complete. <br>
Mitigation: Review and revoke unused Longbridge authorizations when they are no longer needed. <br>


## Reference(s): <br>
- [Longbridge Official Docs](https://open.longbridge.com) <br>
- [Longbridge llms.txt](https://open.longbridge.com/llms.txt) <br>
- [CLI Overview](references/cli/overview.md) <br>
- [MCP Server](references/mcp.md) <br>
- [Python SDK Overview](references/python-sdk/overview.md) <br>
- [Python SDK QuoteContext](references/python-sdk/quote-context.md) <br>
- [Python SDK TradeContext](references/python-sdk/trade-context.md) <br>
- [Rust SDK Overview](references/rust-sdk/overview.md) <br>
- [Rust SDK QuoteContext](references/rust-sdk/quote-context.md) <br>
- [Rust SDK TradeContext](references/rust-sdk/trade-context.md) <br>
- [LLM and AI Integration](references/llm.md) <br>
- [Setup and Authentication](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, configuration examples, and concise analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to call Longbridge CLI, SDK, or MCP tools and to inspect current CLI help before relying on command syntax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
