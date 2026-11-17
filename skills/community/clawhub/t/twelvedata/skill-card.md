## Description:

Twelve Data Official equips agents to retrieve and summarize real-time and historical financial market data for stocks, forex, crypto, ETFs, indices, fundamentals, technical indicators, and portfolio research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twelvedata](https://clawhub.ai/user/twelvedata)

### License/Terms of Use:

MIT

## Use Case:

External users, analysts, traders, and developers use this skill to answer market-data questions, validate symbols, retrieve prices and time series, inspect fundamentals, request technical indicators, and prepare concise financial research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples may expose API keys in command lines, URLs, generated code, logs, shell history, or shared prompts.

Mitigation: Pass credentials through protected environment variables or headers where supported, and avoid placing real API keys in prompts, URLs, logs, or shell history.

Risk: Unpinned package execution or installation can change behavior between runs.

Mitigation: Install only from trusted Twelve Data package sources, prefer pinned package versions, and review packages before deployment.

Risk: The MCP server can access a Twelve Data API key and consume paid quota.

Mitigation: Run the server with least privilege and use it only where access to the API key and quota is acceptable.

## Reference(s):

- [Twelve Data Official ClawHub Page](https://clawhub.ai/twelvedata/skills/twelvedata)
- [Twelve Data Publisher Profile](https://clawhub.ai/user/twelvedata)
- [Twelve Data Website](https://twelvedata.com)
- [Twelve Data API Documentation](https://twelvedata.com/docs)
- [Twelve Data LLM Documentation Index](https://twelvedata.com/docs/llms.txt)
- [Twelve Data MCP Server](https://github.com/twelvedata/mcp)
- [Twelve Data Python SDK](https://github.com/twelvedata/twelvedata-python)
- [LLM Reference Index](references/llms-index.md)
- [Market Data Reference](references/market-data.md)
- [Technical Indicators Reference](references/technical-indicators.md)
- [Fundamentals Reference](references/fundamentals.md)
- [WebSocket Overview](references/websocket/ws-overview.md)
- [AI MCP Server Reference](references/ai/ai-mcp-server.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Twelve Data API key and may consume paid API quota.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
