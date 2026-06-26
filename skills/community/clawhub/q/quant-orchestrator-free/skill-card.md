## Description: <br>
Multi-Agent AI Quant System with factor mining, strategy generation, and automated backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikachu022700](https://clawhub.ai/user/pikachu022700) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to run a BTC-focused strategy research pipeline that collects market data, generates factors and strategy logic, runs a backtest, and reports evaluation metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled Free but includes payment code that can charge an external billing account. <br>
Mitigation: Do not run skill_with_billing.py or provide a user_id unless intending to use SkillPay and accept a possible charge; use the non-billing entry point when no billing is intended. <br>
Risk: The release includes an embedded billing key. <br>
Mitigation: Install only in an isolated environment and rotate or remove the embedded billing key before any trusted deployment. <br>
Risk: Trading metrics may be simulated or unverified. <br>
Mitigation: Treat generated strategy reports and backtest metrics as research output until independently verified against trusted data and assumptions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pikachu022700/quant-orchestrator-free) <br>
- [ClawHub Metadata Homepage](https://clawhub.com/quant-orchestrator) <br>
- [Hyperliquid Market Data Endpoint](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and JSON-like Python dictionaries, with generated strategy code and optional Markdown strategy reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include factor names, generated strategy logic, simulated backtest results, and evaluation metrics such as Sharpe ratio, max drawdown, win rate, IC, and IR.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
