## Description:

Professional quantitative trading system for cryptocurrency - backtesting, paper trading, live trading, and strategy optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading-system builders use this skill to backtest cryptocurrency strategies, optimize parameters, run paper trading, and prepare live trading workflows with explicit risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated video-generation skill file alongside the cryptocurrency trading skill.

Mitigation: Review the package contents before installation and require the publisher to remove or separate unrelated files before release.

Risk: The skill asks users to run unpinned external code.

Mitigation: Pin reviewed repository commits and dependencies before executing setup or trading commands.

Risk: Live trading workflows may use sensitive exchange credentials.

Mitigation: Use testnet or paper trading first, and only use least-privilege, withdrawal-disabled, IP-restricted credentials after live-trading scope is clearly reviewed.

Risk: Commands may pass user-provided strategy or script content to shell workflows.

Mitigation: Avoid shell interpolation of user content and review commands before execution.

## Reference(s):

- [Quant Analyst on ClawHub](https://clawhub.ai/zhenstaff/skills/quant-analyst)
- [openclaw-quant GitHub project](https://github.com/ZhenRobotics/openclaw-quant)
- [openclaw-quant issues](https://github.com/ZhenRobotics/openclaw-quant/issues)
- [openclaw-quant discussions](https://github.com/ZhenRobotics/openclaw-quant/discussions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading-risk cautions, strategy snippets, CLI commands, configuration examples, and performance-analysis summaries.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
