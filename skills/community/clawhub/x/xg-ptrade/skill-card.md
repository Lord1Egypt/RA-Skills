## Description:

小果量化交易Ptrade全能助手 helps users generate Ptrade Python trading strategies, configure backtests, analyze logs and performance, and review trading risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, adapt, and review Ptrade quantitative trading strategies, including dual-moving-average examples, backtest setup, performance review, and trading-log analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact may enable live brokerage automation, account operations, margin or futures actions, IPO or reverse-repo actions, and persistent state behavior beyond simple educational examples.

Mitigation: Separate examples from deployable code, remove or gate high-impact account and trading actions, replace pickle-based state with safe serialization, and test only in a sandbox or backtest account with explicit order confirmations.

Risk: Users may copy strategy templates into Ptrade without enough review for financial, operational, or account-safety consequences.

Mitigation: Require manual review of generated strategy code, backtest settings, order paths, and risk controls before any live trading use.

## Reference(s):

- [Ptrade API 快速入门手册](references/ptrade_api_quickstart.md)
- [双均线策略说明与注意事项](references/strategy_notes.md)
- [Ptrade API 文档](references/ptrade API文档.pdf)
- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-ptrade)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code blocks, configuration notes, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy templates, backtest settings, log analysis, and risk review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
