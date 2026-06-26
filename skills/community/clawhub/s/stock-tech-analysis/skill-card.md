## Description: <br>
Simple technical analysis for stocks using Yahoo Finance data, including SMA20, SMA50, 14-day RSI, 20-day range position, and buy, hold, or sell signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loda13](https://clawhub.ai/user/loda13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to fetch public stock price data and generate concise technical indicator summaries for Yahoo Finance tickers. The output is educational technical analysis and is not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance to fetch public stock data. <br>
Mitigation: Install and run it only in environments where outbound requests to Yahoo Finance are acceptable. <br>
Risk: Technical indicators and buy, hold, or sell signals can be inaccurate or misleading if treated as investment advice. <br>
Mitigation: Use the output for educational analysis only and review market decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loda13/stock-tech-analysis) <br>
- [Yahoo Finance chart data endpoint](https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=3mo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, analysis, guidance] <br>
**Output Format:** [Console text with ticker-level technical summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Yahoo Finance price data and prints moving-average, RSI, range-position, and summary-signal analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
