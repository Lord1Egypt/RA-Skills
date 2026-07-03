## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data with portfolio management, watchlists, dividend analysis, stock scoring, trend scanning, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run finance-analysis workflows for stocks and cryptocurrencies, including ticker analysis, portfolio tracking, watchlist alerts, dividend checks, trend discovery, and rumor scanning. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X integration requires sensitive session credentials. <br>
Mitigation: Use --no-social or skip bird when social sentiment is not needed; if enabled, use a dedicated or low-risk X account and keep AUTH_TOKEN and CT0 out of source control and logs. <br>
Risk: Portfolio and watchlist files can reveal holdings, cost basis, and alert strategy. <br>
Mitigation: Treat generated local JSON files as sensitive and restrict sharing, backups, and permissions accordingly. <br>
Risk: Financial outputs may be incorrect, delayed, or unsuitable for trading decisions. <br>
Mitigation: Use the results for informational analysis only and review against authoritative market data or a licensed financial advisor before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/test-0612) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage guide](artifact/docs/USAGE.md) <br>
- [Hot Scanner documentation](artifact/docs/HOT_SCANNER.md) <br>
- [Architecture documentation](artifact/docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, analysis, files] <br>
**Output Format:** [Markdown and console text with optional JSON output and local JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read market, news, SEC, and optional Twitter/X data; portfolio and watchlist workflows store local JSON files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter version is 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
