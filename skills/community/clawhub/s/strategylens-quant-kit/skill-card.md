## Description:

StrategyLens helps users interpret quantitative trading and futures strategy literature in Chinese, produce runnable Python/pandas backtest templates, explain parameters, cite sources, and use market data for historical backtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingzi6776-cmd](https://clawhub.ai/user/yingzi6776-cmd)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and quantitative researchers use this skill to translate strategy literature into Chinese explanations, runnable backtest templates, parameter notes, and source citations for educational quant research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategies or backtest results may be educationally useful but misleading if treated as investment advice.

Mitigation: Validate results with independent data, paper trading, and human review before relying on them.

Risk: Backtests can understate trading risk when costs, slippage, leverage, futures margin, or market impact are omitted.

Mitigation: Include realistic costs, slippage, leverage assumptions, and risk disclaimers in outputs.

Risk: Connecting broker credentials or trading authority would materially increase operational and financial risk.

Mitigation: Do not connect broker credentials or live trading authority unless the integration receives separate security and compliance review.

## Reference(s):

- [StrategyLens ClawHub Skill Page](https://clawhub.ai/yingzi6776-cmd/skills/strategylens-quant-kit)
- [StrategyLens Homepage](https://clawhub.ai/skill/strategylens)
- [文献深做：期货 / 系统化主线](references/systematic_main.md)
- [量化 / 期货经典策略库（中文解读 + 回测模板 + 参数说明）](references/strategies.md)
- [量化 / 期货 英文文献索引（知识地图）](references/literature.md)
- [文献深做：风险管理](references/risk_management.md)
- [文献深做：期权与衍生品](references/options_volatility.md)
- [文献深做：高频交易与市场微观结构](references/hft_microstructure.md)
- [文献深做：量化基础与工具](references/quant_foundations.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Chinese explanations and Python/pandas code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include source citations and a risk disclaimer; generated strategies and backtests are educational and should be independently validated.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
