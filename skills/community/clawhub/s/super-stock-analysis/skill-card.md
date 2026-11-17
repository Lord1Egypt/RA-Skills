## Description:

Analyzes stocks and cryptocurrencies using Yahoo Finance data with portfolio tracking, watchlists, dividend analysis, multi-factor scoring, trend detection, and early-signal scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request stock, crypto, income, portfolio, watchlist, trend, and rumor/signal analysis from command-line market data workflows. The outputs are informational analysis and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional social scanning can require X session cookies and broad local access.

Mitigation: Use the skill without the social scanner unless you have reviewed the flow; avoid granting Terminal Full Disk Access and avoid storing X cookies in the skill directory.

Risk: The artifact includes local file-modifying code and portfolio or watchlist storage.

Mitigation: Do not run batch_refactor.py during normal use, and keep portfolio or watchlist data in a private directory with restrictive permissions.

Risk: Market analysis, trend, and rumor outputs can be delayed, incomplete, or misleading.

Mitigation: Treat outputs as informational signals only and verify investment decisions with qualified financial advice and authoritative market sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-stock-analysis)
- [Publisher profile](https://clawhub.ai/user/subaru0573)
- [MarketPulse homepage](https://marketpulse.io)
- [Usage guide](docs/USAGE.md)
- [Concept and philosophy](docs/CONCEPT.md)
- [Technical architecture](docs/ARCHITECTURE.md)
- [Hot scanner documentation](docs/HOT_SCANNER.md)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal text, and optional JSON from supporting scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market and social outputs may depend on third-party data availability, local credentials, and cache timing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
