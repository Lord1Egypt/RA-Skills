## Description: <br>
StockBuddy helps agents analyze CN, HK, and US equities, review portfolios, track account cash and positions, and produce execution-aware buy, sell, hold, and watchlist guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tacitlab](https://clawhub.ai/user/tacitlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use StockBuddy to analyze individual equities, review portfolios, manage watchlists, positions, accounts, and cash balances, and convert user-confirmed trading constraints into practical non-advisory execution guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency setup can alter system Python packages. <br>
Mitigation: Review scripts/install_deps.sh before use and prefer installing dependencies in a virtual environment. <br>
Risk: Automatic database migration can delete stored positions. <br>
Mitigation: Back up ~/.stockbuddy/stockbuddy.db before first use, upgrade, or migration. <br>
Risk: The skill can read or modify portfolio, account, cash, and watchlist data. <br>
Mitigation: Confirm user intent before allowing portfolio, account, cash, or watchlist changes. <br>
Risk: Market data and analysis can be delayed, incomplete, or unsuitable as investment advice. <br>
Mitigation: Treat outputs as reference material, verify market data independently, and include the required risk disclaimer in final analysis. <br>


## Reference(s): <br>
- [StockBuddy ClawHub Page](https://clawhub.ai/tacitlab/stockbuddy) <br>
- [Output Templates](references/output_templates.md) <br>
- [Technical Indicators](references/technical_indicators.md) <br>
- [Data Source Roadmap](references/data-source-roadmap.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with short bullets or tables; helper scripts emit JSON when run directly.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local portfolio, account, cash, watchlist, and cache data in SQLite; financial analysis should be treated as reference material and include a risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
