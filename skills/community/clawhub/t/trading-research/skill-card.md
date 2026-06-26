## Description: <br>
Binance cryptocurrency trading research, technical analysis, and position management. Triggers on requests for crypto prices, market data, trading analysis, DCA planning, position sizing, whale activity, or any trading research questions about Bitcoin, altcoins, or crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fpsjago](https://clawhub.ai/user/fpsjago) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to research Binance cryptocurrency markets, run technical analysis, plan DCA schedules, size positions, scan market opportunities, and summarize whale activity. Outputs are informational trading research and should not be treated as personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading analysis may be mistaken for personalized financial advice or used to make high-risk decisions. <br>
Mitigation: Treat outputs as informational research only, require human review before acting, and apply independent financial judgment and risk controls. <br>
Risk: The skill contacts Binance public APIs and may be unavailable or restricted in some regions. <br>
Mitigation: Use only where Binance API access is permitted, do not bypass regional restrictions, and expect graceful failure when endpoints are blocked or unavailable. <br>
Risk: Reference material includes examples for authenticated Binance account access and order placement. <br>
Mitigation: Do not provide live API keys or execute account/order workflows without separate code review, least-privilege keys, testnet or dry-run safeguards, and explicit human confirmation. <br>
Risk: Market data is snapshot-based REST data and may become stale or incomplete. <br>
Mitigation: Refresh data before decisions, compare against other sources when appropriate, and include caveats about timing and market volatility. <br>


## Reference(s): <br>
- [Trading Research on ClawHub](https://clawhub.ai/fpsjago/trading-research) <br>
- [Binance API Quick Reference](references/binance-api.md) <br>
- [Technical Indicators Reference](references/indicators.md) <br>
- [Trading Strategies Reference](references/strategies.md) <br>
- [Binance public market data API](https://data-api.binance.vision) <br>
- [Binance futures public API](https://fapi.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output, with optional JSON from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Binance public API calls for market data and locally calculated trading research outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
