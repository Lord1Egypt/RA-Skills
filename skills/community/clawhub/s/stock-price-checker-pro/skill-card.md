## Description: <br>
Fetches current stock, ETF, index, and crypto market data from Yahoo Finance and formats prices, ranges, volume, news, and upcoming events for an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to answer current market-price questions for stocks, ETFs, indexes, and crypto tickers. It is suited for quick price checks, recent range summaries, volume context, company-specific headlines, and upcoming event dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and installs yfinance through uv before contacting Yahoo Finance. <br>
Mitigation: Review the artifact and pin or approve the yfinance dependency before first use when tighter supply-chain control is required. <br>
Risk: Market data, headlines, and event dates may be unavailable, delayed, or limited by Yahoo Finance or yfinance behavior. <br>
Mitigation: Treat outputs as market-data summaries from Yahoo Finance and verify time-sensitive financial decisions against an authoritative source. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style market summary with links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ticker symbol; live market data, news, and events depend on Yahoo Finance availability through yfinance.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
