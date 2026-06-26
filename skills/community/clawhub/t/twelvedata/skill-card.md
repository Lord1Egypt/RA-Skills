## Description: <br>
Official Twelve Data integration for OpenClaw and ClawHub that helps agents retrieve real-time and historical financial market data, quotes, time series, technical indicators, fundamentals, symbol search results, and portfolio or research outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twelvedata](https://clawhub.ai/user/twelvedata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, analysts, traders, and investors use this skill to ask an agent for Twelve Data-backed market data, technical analysis, fundamentals, symbol lookup, and portfolio research. It is suited for workflows that need current or historical data across stocks, forex, crypto, ETFs, indices, mutual funds, commodities, and related instruments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial market data can be delayed, unavailable, plan-limited, or incomplete for a requested instrument or venue. <br>
Mitigation: Validate symbols, note timezones and data availability, handle missing values clearly, and avoid presenting outputs as investment advice. <br>
Risk: API keys can be exposed through prompts, shared code, shell history, or URLs. <br>
Mitigation: Use the MCP server or header/environment-based secret handling, keep keys out of generated text, and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [Twelve Data Website](https://twelvedata.com) <br>
- [Twelve Data ClawHub Repository](https://github.com/twelvedata/twelvedata-clawhub) <br>
- [Twelve Data API Documentation](https://twelvedata.com/docs) <br>
- [Twelve Data LLM Documentation Index](references/llms-index.md) <br>
- [Market Data Reference](references/market-data.md) <br>
- [Technical Indicators Reference](references/technical-indicators.md) <br>
- [Fundamentals Reference](references/fundamentals.md) <br>
- [MCP Server Reference](references/ai/ai-mcp-server.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, summaries, inline code, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite Twelve Data as the data source and may include API or MCP setup guidance when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
