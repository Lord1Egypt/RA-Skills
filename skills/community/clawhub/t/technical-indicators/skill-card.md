## Description: <br>
Technical Indicators calculates A-share technical indicators, volume-price patterns, resonance signals, market sentiment, position sizing, and backtest summaries for trading analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBABYZS](https://clawhub.ai/user/GBABYZS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-analysis agents use this skill to compute A-share technical indicators, evaluate multi-indicator signals, run backtests, and produce risk-aware position guidance. Outputs are informational and should be reviewed before any trading decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches market data from external financial-data providers that may be delayed, unavailable, or changed by the provider. <br>
Mitigation: Confirm data freshness and provider availability before relying on outputs, and use caching or fallback handling for production workflows. <br>
Risk: Generated trading signals, sentiment scores, model forecasts, and backtests may be misleading if treated as verified investment advice. <br>
Mitigation: Use outputs as informational analysis only, review assumptions and recent market context, and require qualified human approval before trading. <br>
Risk: Forum, news, policy, and market sentiment components may rely on simplified proxies or neutral defaults rather than full text analysis. <br>
Mitigation: Validate sentiment-sensitive conclusions against primary news, filings, and market sources before acting on them. <br>


## Reference(s): <br>
- [Technical Indicators Skill Page](https://clawhub.ai/GBABYZS/technical-indicators) <br>
- [Artifact README](artifact/README.md) <br>
- [Technical Indicators Skill Documentation](artifact/SKILL.md) <br>
- [Market Sentiment Documentation](artifact/README_MARKET_SENTIMENT.md) <br>
- [LSTM Predictor Documentation](artifact/README_LSTM.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON-like analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces technical indicators, trading-signal scores, sentiment summaries, backtest metrics, and position-sizing recommendations from market data inputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
