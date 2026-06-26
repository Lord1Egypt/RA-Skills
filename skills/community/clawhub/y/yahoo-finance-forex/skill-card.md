## Description: <br>
Fetches real-time FOREX news and market data from Yahoo Finance for major currency pairs (EUR/USD, GBP/USD, USD/JPY, etc.). Analyzes sentiment and provides trading context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nazimboudeffa](https://clawhub.ai/user/nazimboudeffa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to fetch Yahoo Finance market data and recent news for seven major FOREX pairs, then summarize rates, headlines, keyword sentiment, and trading context. BUY, SELL, and HOLD labels should be treated as educational sentiment indicators, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script installs and imports the external yfinance package and makes network requests for Yahoo Finance market data. <br>
Mitigation: Review the dependency and run the script only in environments where outbound market-data requests are acceptable. <br>
Risk: BUY, SELL, and HOLD outputs may be mistaken for financial advice. <br>
Mitigation: Present these labels as educational keyword-sentiment signals and require independent research before any trading decision. <br>
Risk: Keyword-based headline sentiment can miss nuance, source quality, and whether news is already priced in. <br>
Mitigation: Cross-check headlines, timestamps, market context, and technical or fundamental analysis before relying on the signal. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nazimboudeffa/yahoo-finance-forex) <br>
- [API Examples](references/api-examples.md) <br>
- [FOREX Pairs Reference](references/forex-pairs.md) <br>
- [Sentiment Analysis Guide](references/sentiment-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include current rate, percent change, recent Yahoo Finance news, timestamp, keyword sentiment score, and BUY/SELL/HOLD label.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
