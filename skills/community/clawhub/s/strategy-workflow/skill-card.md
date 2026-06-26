## Description: <br>
Comprehensive strategy development workflow from ideation to validation for creating trading strategies, running backtests, parameter optimization, and walk-forward validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahuserious](https://clawhub.ai/user/ahuserious) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, quantitative researchers, and trading-system operators use this skill to move from strategy hypothesis through GPU-accelerated backtesting, optimization, validation, and reporting. The workflow is intended to guide agent-assisted execution of trading research and operational runbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can encourage high-authority operations such as persistent watchdogs, worker kill/relaunch behavior, startup hooks, and autonomous remediation. <br>
Mitigation: Require explicit human approval before launching watchdogs, startup hooks, or autonomous repair loops, and run them only in an isolated machine or disposable cloud instance. <br>
Risk: The artifact includes SSH/SCP and cloud execution paths that may affect remote systems or expose credentials and data. <br>
Mitigation: Review every remote command and referenced script before use, avoid root SSH unless required, and keep credentials and trading data out of agent-visible logs. <br>
Risk: The workflow references private documentation ingest, backups, exports, and state/log artifacts. <br>
Mitigation: Get approval before ingesting private documentation or exporting artifacts, and limit retained logs and backups to the minimum required for reproducibility. <br>


## Reference(s): <br>
- [Strategy Generation Reference](artifact/references/strategy_generation.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ahuserious/strategy-workflow) <br>
- [VectorBT Documentation](https://vectorbt.dev/) <br>
- [NautilusTrader Documentation](https://nautilustrader.io/) <br>
- [Optuna Documentation](https://optuna.readthedocs.io/) <br>
- [QuantStats Repository](https://github.com/ranaroussi/quantstats) <br>
- [TradingView Bollinger Bands Reference](https://www.tradingview.com/support/solutions/43000501840/) <br>
- [TradingView CCI Stochastic Reference](https://www.tradingview.com/script/XZyG5SOx-CCI-Stochastic-and-a-quick-lesson-on-Scalping-Trading-Systems/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local or remote execution steps, watchdog operation, and state/log artifact review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
