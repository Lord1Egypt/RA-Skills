## Description:

小果全能大QMT量化交易助手 helps agents generate, review, and troubleshoot QMT quantitative trading strategy code for backtesting and live-trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading users use this skill to produce QMT strategy code, QMT API usage guidance, backtest templates, live-trading templates, and troubleshooting advice for QMT scripts. The skill is especially oriented toward Chinese-market QMT workflows involving stocks, futures, options, ETFs, convertible bonds, margin trading, market data access, and order placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled QMT examples and scripts can generate or execute live-trading order logic.

Mitigation: Review scripts before installation, run in QMT simulation first, and require explicit live-trading controls before connecting a brokerage account.

Risk: Authorization values may be handled unsafely in some bundled scripts.

Mitigation: Remove plaintext HTTP endpoints and credential logging, replace hardcoded or shared authorization values, and use account allowlists.

Risk: Automated strategies may place unintended orders if limits and emergency controls are absent.

Mitigation: Add order limits, account allowlists, and a kill switch before enabling real brokerage execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-qmt)
- [Publisher profile](https://clawhub.ai/user/li152)
- [QMT assistant handbook](references/小果全能大QMT量化助手.txt)
- [Trading order functions](references/9交易下单函数.txt)
- [Trading query functions](references/10交易查询函数.txt)
- [Live trading setup](references/2如何实盘运行一个python策略.txt)
- [Common QMT issues](references/63常见问题.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with Python code blocks and QMT configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include executable QMT strategy snippets and live-trading order logic that require review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
