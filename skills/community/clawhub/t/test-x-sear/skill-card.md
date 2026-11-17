## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists with alerts, dividend analysis, stock scoring, viral trend detection, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run market research workflows for stocks and cryptocurrencies, including ticker analysis, portfolio tracking, watchlist alerts, dividend review, trending asset scans, and rumor monitoring. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanning handles browser-session credentials and passes broad environment secrets to an external CLI.

Mitigation: Use core stock, dividend, portfolio, and watchlist features without social scanning when possible; run scans with --no-social and avoid storing unrelated secrets in the skill .env file.

Risk: Stored portfolio and watchlist data may contain financial holdings or trading preferences.

Mitigation: Limit stored data to what is needed for analysis, protect local skill data files, and avoid granting unnecessary filesystem access.

Risk: Market, news, and social signals can be delayed, incomplete, or misleading.

Mitigation: Treat outputs as informational research, verify against authoritative sources, and consult a licensed financial advisor before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/test-x-sear)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)
- [Hot Scanner documentation](docs/HOT_SCANNER.md)
- [Usage documentation](docs/USAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output, with optional JSON output from scanner workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio and watchlist JSON files under the user's skill data directory.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
