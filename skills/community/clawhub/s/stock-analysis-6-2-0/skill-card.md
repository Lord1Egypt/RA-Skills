## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squally2k](https://clawhub.ai/user/squally2k)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate stock and cryptocurrency analysis, compare tickers, track portfolios and watchlists, inspect dividends, scan trending assets, and surface early market rumors. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X social scanning can expose live X session credentials to a third-party CLI.

Mitigation: Use --no-social for hot scans unless you have reviewed and accepted that access, and do not place unrelated secrets in the skill .env.

Risk: Portfolio and watchlist files may contain sensitive local financial data.

Mitigation: Treat these files as sensitive data, restrict local access, and avoid granting Terminal Full Disk Access unless it is necessary.

Risk: Market analysis, rumors, and trend signals may be delayed, incomplete, or incorrect.

Mitigation: Use the output for informational screening only, verify material facts with authoritative sources, and consult a licensed financial advisor before making investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/squally2k/skills/stock-analysis-6-2-0)
- [Publisher Profile](https://clawhub.ai/user/squally2k)
- [Artifact README](artifact/README.md)
- [Usage Guide](artifact/docs/USAGE.md)
- [Hot Scanner Guide](artifact/docs/HOT_SCANNER.md)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, console reports, and optional JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local portfolio and watchlist JSON files; market data and some sentiment inputs can be delayed.]

## Skill Version(s):

6.2.0 (source: artifact/SKILL.md frontmatter; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
