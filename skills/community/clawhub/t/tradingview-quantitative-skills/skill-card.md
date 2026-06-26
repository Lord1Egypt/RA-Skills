## Description: <br>
Professional quantitative investment analysis system based on TradingView data that provides intelligent stock screening, technical pattern recognition, market review, risk management, event-driven analysis, multi-factor scoring, and trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hypier](https://clawhub.ai/user/hypier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze markets, screen securities, review technical and fundamental signals, monitor news and events, and produce risk-aware trading research from TradingView data through a configured MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce buy/sell, options, stop-loss, target-price, or position-sizing outputs that may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as research prompts, verify conclusions independently, and make investment decisions cautiously. <br>
Risk: Using the configured MCP service may send market symbols, news queries, and related analysis requests to TradingView or RapidAPI. <br>
Mitigation: Install only when this data sharing is acceptable, and review applicable external service terms and privacy practices. <br>
Risk: RapidAPI or service tokens can be exposed if placed directly in shared configuration files or logs. <br>
Mitigation: Keep API keys private, prefer environment variables or protected configuration files, and avoid committing credentials to version control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hypier/tradingview-quantitative-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/hypier) <br>
- [TradingView Data API on RapidAPI](https://rapidapi.com/hypier/api/tradingview-data1) <br>
- [TradingView Data API](references/api-documentation.md) <br>
- [MCP Tools Usage Guide](references/mcp-tools-guide.md) <br>
- [Technical Analysis Methodology](references/technical-analysis.md) <br>
- [Technical Pattern Recognition Library](references/pattern-library.md) <br>
- [Risk Management System](references/risk-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline tool-call examples, JSON configuration snippets, and natural-language analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces research-oriented market analysis, screening results, risk notes, and configuration guidance; outputs are not personalized financial advice.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
