## Description: <br>
Comprehensive A-share and Hong Kong stock analysis toolkit for OpenClaw agents, covering technical indicators, multi-source market data, news aggregation, watchlists, and integrated reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oldairman](https://clawhub.ai/user/oldairman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and OpenClaw agents use this skill to analyze Chinese A-share and Hong Kong stocks, generate technical summaries, search recent news, maintain watchlists, and produce market or research reports. Outputs are informational and should be reviewed before any investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols, watchlists, and news queries may be sent to external finance or search services. <br>
Mitigation: Use only in environments where those queries are acceptable to share, and review optional data-source or search integrations before enabling them. <br>
Risk: Local watchlist, report, and analysis-log files can contain sensitive research history. <br>
Mitigation: Store the skill in an appropriate workspace and clear local watchlist or analysis-log files when the research history should not persist. <br>
Risk: Generated market signals and buy, hold, or sell language may be incomplete or misleading. <br>
Mitigation: Treat outputs as informational analysis, verify source data and assumptions, and consult qualified financial advice before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oldairman/xia-china-stock) <br>
- [Publisher profile](https://clawhub.ai/user/oldairman) <br>
- [Popular Chinese Stocks Reference](references/china-stocks.md) <br>
- [Eastmoney](https://www.eastmoney.com) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and tables, JSON summaries, and shell commands for running analysis scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local watchlist, report, or analysis-log files when users run the included scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
