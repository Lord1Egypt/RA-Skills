## Description:

Tai Alpha stock analysis - collect, VectorBT backtest (RSI/MACD/BB), conviction score, optional ML, and SQLite persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cplog](https://clawhub.ai/user/cplog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run ticker-level market data collection, backtests, conviction scoring, optional ML estimates, persona overlays, reports, alerts, and portfolio or sector comparisons. Outputs are informational and are not financial, tax, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data may be delayed, sparse, or incorrect, especially outside the primary US-listed symbol target.

Mitigation: Treat reports as informational only, verify source data independently, and review jurisdiction-specific market data terms before operational use.

Risk: Backtests, conviction scores, and optional ML estimates can be misleading if interpreted as forecasts or recommendations.

Mitigation: Review assumptions, slippage, fees, liquidity, and model limitations before acting; do not use outputs as financial advice.

Risk: The skill writes analysis and alert data to a local SQLite database and may perform market-data network calls.

Mitigation: Run in an appropriate environment, configure database paths deliberately, and avoid storing sensitive watchlists or credentials in shared workspaces.

Risk: The optional publishing helper installs or invokes publishing tooling and deserves extra caution.

Mitigation: Run publishing helpers only in isolated environments with scoped credentials, or replace runtime dependency installation with a locked and reviewed dependency flow.

## Reference(s):

- [Tai Alpha Stock on ClawHub](https://clawhub.ai/cplog/skills/tai-alpha-stock)
- [Publisher profile](https://clawhub.ai/user/cplog)
- [Setup and docs](setup/README.md)
- [User flow](setup/USERFLOW.md)
- [API reference](setup/docs/guides/API_REFERENCE.md)
- [SQLite storage](setup/docs/database/SQLITE.md)
- [Disclaimer and limitations](setup/docs/guides/DISCLAIMER_AND_LIMITATIONS.md)
- [openclaw stock-analysis inspiration](https://github.com/openclaw/skills/tree/main/skills/udiedrichsen/stock-analysis)
- [UZI-Skill inspiration](https://github.com/wbh604/UZI-Skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON-like analysis payloads, SQLite records, and generated reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch market data from Yahoo/yfinance and optional CoinGecko; analysis runs are persisted to a local SQLite database unless configured otherwise.]

## Skill Version(s):

1.33.1 (source: release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
