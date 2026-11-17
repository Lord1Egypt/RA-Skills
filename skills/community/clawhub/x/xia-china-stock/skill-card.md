## Description:

Comprehensive A-share and Hong Kong stock analysis toolkit for OpenClaw agents, including technical indicators, multi-source market data, news aggregation, watchlists, and integrated reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oldairman](https://clawhub.ai/user/oldairman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Chinese A-share and Hong Kong stocks, generate technical summaries and market reports, search recent news, and maintain watchlists with alert-oriented signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search fallbacks may invoke locally discovered mcporter or Tavily tooling.

Mitigation: Review and explicitly configure or disable those optional backends unless the local tools and their data handling are trusted.

Risk: Stock symbols, company names, and search queries may be sent to external finance or search services.

Mitigation: Avoid entering confidential portfolio data and run the skill only in environments where external market-data requests are acceptable.

Risk: Watchlist and analysis files can retain stock-interest history on the local machine.

Mitigation: Use an isolated environment and periodically review or remove local watchlist and analysis files when no longer needed.

Risk: The skill produces market analysis and recommendation-style signals that may be incomplete or delayed.

Mitigation: Treat outputs as informational, verify data against authoritative sources, and consult qualified financial advice before making investment decisions.

## Reference(s):

- [China Stocks Reference](artifact/references/china-stocks.md)
- [ClawHub Skill Page](https://clawhub.ai/oldairman/skills/xia-china-stock)
- [Eastmoney](https://www.eastmoney.com)
- [Xueqiu](https://xueqiu.com)
- [Yahoo Finance](https://finance.yahoo.com)
- [Google Finance](https://www.google.com/finance)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON from command-line analysis scripts, with shell command examples and report templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include technical indicators, quote data, news summaries, buy/hold/sell-style signals, watchlist alerts, and financial-risk disclaimers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
