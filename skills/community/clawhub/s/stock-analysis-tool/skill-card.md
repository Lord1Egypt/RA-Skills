## Description: <br>
Analyzes stocks and funds across A-share, Hong Kong, U.S. and fund markets using technical indicators, MACD divergence checks, and a quantitative scoring system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[write31bug](https://clawhub.ai/user/write31bug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run a Python CLI for technical analysis of stocks, ETFs, LOFs, and open-end funds across A-share, Hong Kong, and U.S. markets. It supports single-symbol analysis, batch analysis, watchlists, JSON output, terminal tables, and offline test mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data comes from public finance providers and may be delayed, unavailable, or unsuitable as the sole basis for trading decisions. <br>
Mitigation: Treat outputs as technical-analysis reference material, not investment advice, and verify prices and signals with authoritative market data before acting. <br>
Risk: The CLI contacts public finance data providers and writes a watchlist/config file in the user's home directory. <br>
Mitigation: Run it in a controlled environment with expected network access only, and review ~/.stock-analysis/config.json if watchlist commands are used. <br>
Risk: Dependencies are specified with broad minimum versions, which can make builds vary over time. <br>
Mitigation: Use a virtual environment and pin or lock dependency versions for repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/write31bug/stock-analysis-tool) <br>
- [Publisher profile](https://clawhub.ai/user/write31bug) <br>
- [Project homepage](https://github.com/write31bug/stock-technical-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus CLI output as terminal tables, ASCII text, JSON, or user-specified files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Watchlist commands store local configuration under ~/.stock-analysis/config.json; analysis commands may contact public finance data providers.] <br>

## Skill Version(s): <br>
1.8.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
