## Description: <br>
Provides multi-market stock analysis with quotes, technical indicators, news sentiment, and buy/sell/hold recommendations for portfolios and indices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and automation agents use this skill to review stock watchlists, portfolios, and market indices with market data, technical signals, and news sentiment. Its recommendations are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols, watchlists, and news searches may be sent to external market data or search providers. <br>
Mitigation: Configure only the API keys and providers needed for the deployment, and avoid submitting sensitive portfolio information when provider sharing is not acceptable. <br>
Risk: Generated buy, sell, or hold recommendations may be incorrect, delayed, or unsuitable for a user's financial situation. <br>
Mitigation: Treat analysis as informational, verify prices and signals independently, and require human review before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leohuang8688/stock-analysis-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain-text or Markdown-style stock analysis report with prices, indicators, sentiment, recommendations, and rationale.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured stock list and may use optional API keys for Tavily, Alpha Vantage, and Tushare data sources.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
