## Description:

Fetch TradingView market data, including historical OHLCV bars, live price streams, symbol search, technical indicators, and statistical analysis for stocks, crypto, forex, futures, indices, and commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarun-khatri](https://clawhub.ai/user/tarun-khatri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading researchers use this skill to fetch market data, stream live prices, resolve TradingView symbols, compute indicators, compare assets, and export data for analysis or backtesting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use and locally store a TradingView browser token.

Mitigation: Prefer anonymous mode or environment variables over saved tokens, avoid passing tokens in shell commands, and review token storage before installation.

Risk: The skill runs a SessionStart hook that performs automatic configuration, credential, cache-directory, and network checks.

Mitigation: Review or disable the startup hook if automatic credential checks or network probes are not desired.

Risk: The skill contacts TradingView and fallback data providers and writes cache/config files under the user's home directory.

Mitigation: Install only in environments where these network calls and local file writes are acceptable, and configure cache paths explicitly when needed.

## Reference(s):

- [Project homepage](https://github.com/tarun-khatri/tvfetch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries with tables, inline shell commands, code snippets, and optional CSV, JSON, or Parquet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market-data warnings, source attribution, authentication mode, cache status, and export paths]

## Skill Version(s):

1.0.0 (source: frontmatter, pyproject.toml, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
