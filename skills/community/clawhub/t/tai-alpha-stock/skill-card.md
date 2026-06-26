## Description: <br>
Tai Alpha stock analysis - collect market data, run VectorBT backtests for RSI/MACD/BB strategies, generate conviction scores, and optionally run ML with SQLite persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cplog](https://clawhub.ai/user/cplog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run ticker-level stock analysis workflows that collect market data, backtest strategies, score conviction, produce reports, and persist runs to SQLite for later inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data calls and optional crypto scanning may contact external data services and return delayed, sparse, or unavailable data. <br>
Mitigation: Install only when those network calls are acceptable, review data-source terms, and treat generated analysis as informational rather than investment advice. <br>
Risk: Analysis runs are persisted to a local SQLite database that may contain ticker analyses and watchlist data. <br>
Mitigation: Set TAI_ALPHA_DB_PATH or TAI_ALPHA_OUTPUT_DIR to an approved storage location and manage the database according to local retention and access requirements. <br>
Risk: Backtests, conviction scores, and optional ML output can be mistaken for validated financial recommendations. <br>
Mitigation: Use the reports as decision-support material only, review the documented limitations, and consult appropriate professionals before making investment decisions. <br>


## Reference(s): <br>
- [Tai Alpha Stock ClawHub listing](https://clawhub.ai/cplog/tai-alpha-stock) <br>
- [Setup README](setup/README.md) <br>
- [User Flow](setup/USERFLOW.md) <br>
- [Disclaimer and Limitations](setup/docs/guides/DISCLAIMER_AND_LIMITATIONS.md) <br>
- [SQLite documentation](setup/docs/database/SQLITE.md) <br>
- [Persona ecosystem guide](setup/docs/guides/PERSONA_ECOSYSTEM_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, text reports, JSON score output, and SQLite-backed run records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational stock-analysis artifacts and may depend on external market-data availability and local SQLite storage.] <br>

## Skill Version(s): <br>
1.33.1 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
