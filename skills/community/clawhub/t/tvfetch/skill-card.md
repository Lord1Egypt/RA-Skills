## Description: <br>
Fetches TradingView market data, including historical OHLCV bars, live price streams, symbol search, technical indicators, and statistical analysis for stocks, crypto, forex, futures, indices, and commodities. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[tarun-khatri](https://clawhub.ai/user/tarun-khatri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market-data users use TVFetch to fetch or stream TradingView market data, export OHLCV datasets, and generate technical-analysis summaries through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TradingView session tokens may be stored under ~/.tvfetch/.env and local .env files can influence authentication. <br>
Mitigation: Prefer anonymous mode when possible, avoid --token on shared systems, review ~/.tvfetch/.env permissions, and avoid running from untrusted project directories. <br>
Risk: The skill contacts TradingView and optional fallback market-data providers and writes cache data under ~/.tvfetch. <br>
Mitigation: Use it only in environments where those outbound connections and local cache writes are acceptable, and review network and cache policy before deployment. <br>
Risk: The artifact states that use of the reverse-engineered TradingView protocol may violate TradingView terms. <br>
Mitigation: Confirm applicable TradingView and fallback-provider terms before operational use, especially outside personal or educational workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tarun-khatri/tvfetch) <br>
- [Project homepage](https://github.com/tarun-khatri/tvfetch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown responses with tables, inline shell commands, JSON summaries, and optional CSV, JSON, or Parquet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use anonymous mode, optional TradingView session tokens, local SQLite caching under ~/.tvfetch, and user-selected export paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
