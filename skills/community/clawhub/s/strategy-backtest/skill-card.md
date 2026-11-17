## Description:

Guides agents through quantitative trading strategy backtesting, parameter tuning, and reporting workflows using historical data and explicit assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to structure backtest specifications, run or review strategy workflow commands, compare parameters, and produce concise Markdown reports with assumptions and caveats. Users should verify all metrics from actual execution output before relying on any result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled tool returns success messages and stores command arguments without computing full backtest results or reports.

Mitigation: Treat generated records as workflow logs, verify any metrics with a real backtesting engine, and do not present logged success messages as investment analysis.

Risk: Command inputs may contain private dataset paths, account identifiers, proprietary strategy details, or other sensitive information.

Mitigation: Avoid passing secrets or confidential strategy data, and test the skill only in an isolated environment.

Risk: Trading strategy backtests can be misleading when costs, slippage, survivorship bias, or overfitting are not handled explicitly.

Mitigation: Document assumptions, validate out of sample, and include limitations in any report.

## Reference(s):

- [Strategy Backtest Guide](references/strategy_backtest_guide.md)
- [Backtrader Documentation](https://www.backtrader.com/docu/)
- [Backtrader on GitHub](https://github.com/mementum/backtrader)
- [Hacker News Backtesting Pitfalls Discussion](https://news.ycombinator.com/item?id=39462946)
- [Reddit r/algotrading Discussion](https://www.reddit.com/r/algotrading/comments/1073140yyz/quant_backtest_ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, JSON command output, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backtest metrics must be grounded in actual run output; command inputs may be stored locally by the bundled tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
