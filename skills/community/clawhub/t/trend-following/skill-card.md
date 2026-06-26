## Description: <br>
Trend-following stock analysis using price and volume to generate buy/sell signals, support and resistance levels, entry and exit targets, and risk/reward information for Yahoo Finance tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run command-line trend analysis for a stock ticker and summarize current trend status, key levels, trading signals, and targets. It is intended as informational analysis that should be validated with current market data before trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buy/sell signals, targets, and stop-loss output could be mistaken for financial advice. <br>
Mitigation: Treat results as informational analysis only and validate with current market data and appropriate financial review before trading. <br>
Risk: The skill fetches public market data over the network and depends on the third-party yfinance package. <br>
Mitigation: Install only where network market-data access is acceptable and review the yfinance dependency before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with indicator values, signal lists, support and resistance levels, and target prices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ticker symbol and optionally accepts a Yahoo Finance period such as 3mo, 6mo, 1y, 2y, or 5y.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
