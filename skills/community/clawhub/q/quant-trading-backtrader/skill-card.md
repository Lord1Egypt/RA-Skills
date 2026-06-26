## Description: <br>
Build, backtest, and optimize quantitative trading strategies in Python using Backtrader with support for indicators, risk management, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmsx000-cloud](https://clawhub.ai/user/gmsx000-cloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to create Backtrader-based strategy templates, run local historical backtests, and add common controls such as indicators, stop-loss orders, position sizing, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could treat the included strategy or backtest output as financial advice or a live-trading system. <br>
Mitigation: Use the strategy as a simulation example only, review assumptions and data quality, and require independent financial and operational validation before any trading use. <br>
Risk: Unverified Python dependencies could introduce supply-chain or environment hygiene issues. <br>
Mitigation: Install and run the skill in a virtual environment and verify the Backtrader and matplotlib packages before use. <br>
Risk: Backtests can overfit historical data and produce misleading expectations. <br>
Mitigation: Use walk-forward analysis, test on unseen data, and keep risk controls such as stop-loss rules and position sizing explicit. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/gmsx000-cloud/quant-trading-backtrader) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [SMA crossover example](artifact/examples/sma_crossover.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Backtrader backtesting guidance and example Python strategy code; it does not provide live trading execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
