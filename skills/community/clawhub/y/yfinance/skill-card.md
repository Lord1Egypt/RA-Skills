## Description: <br>
Fetch live and historical stock data from Yahoo Finance, optimized for Indonesia IDX stocks, including prices, OHLCV history, fundamentals, dividends, and stock splits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[temmyraharjo](https://clawhub.ai/user/temmyraharjo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market analysts use this skill to query Yahoo Finance data through a local connector, with convenience handling for Indonesian IDX tickers. It supports price checks, historical chart data, company fundamentals, dividend history, and stock split history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts a local web server for Yahoo Finance queries, which can expose port 8000 if bound broadly or deployed on a public host. <br>
Mitigation: For local use, bind the server to 127.0.0.1, keep port 8000 off the public internet, and stop the uvicorn process when finished. <br>
Risk: Ticker symbols without a suffix are automatically interpreted as Indonesian IDX symbols. <br>
Mitigation: Use explicit market suffixes for non-Indonesian securities or set auto_jk=false when querying global tickers. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/temmyraharjo/yfinance) <br>
- [Local OpenAPI connector specification](artifact/openapi.json) <br>
- [Release README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with human-readable formatted text, plus Markdown guidance and shell commands for local setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local FastAPI server on port 8000 and queries Yahoo Finance through yfinance; ticker symbols without a suffix default to IDX .JK unless auto_jk=false is used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
