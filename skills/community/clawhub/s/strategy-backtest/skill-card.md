## Description: <br>
Quantitative strategy backtesting for implementing, running, and tuning trading rules on historical data, with performance metrics such as CAGR, max drawdown, Sharpe ratio, win rate, and simple parameter sweeps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and quantitative trading practitioners use this skill to run backtests, optimize strategy parameters, and produce reports grounded in actual run outputs rather than invented metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI can install and run analysis tooling and save experiment history on the user's machine. <br>
Mitigation: Run it in a controlled local environment, use read-only connector credentials, and avoid storing sensitive experiment payloads unless required. <br>
Risk: Backtest outputs can be misleading if costs, slippage, survivorship bias, data adjustments, or overfitting are not addressed. <br>
Mitigation: Base reports only on actual run outputs, document assumptions, validate optimized parameters out of sample, and treat results as research rather than investment advice. <br>


## Reference(s): <br>
- [Strategy Backtest Framework & Guide](references/strategy_backtest_guide.md) <br>
- [Backtrader documentation](https://www.backtrader.com/docu/) <br>
- [Backtrader on GitHub](https://github.com/mementum/backtrader) <br>
- [Hacker News - backtesting pitfalls](https://news.ycombinator.com/item?id=39462946) <br>
- [Reddit r/algotrading discussion](https://www.reddit.com/r/algotrading/comments/1073140yyz/quant_backtest_ai/) <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/strategy-backtest) <br>
- [Publisher profile](https://clawhub.ai/user/mikeclaw007) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON CLI output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should state assumptions for fees, spreads, leverage, time zones, data quality, and metric definitions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
