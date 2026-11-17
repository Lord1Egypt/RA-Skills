## Description:

加密交易机器人 helps agents support cryptocurrency strategy development, historical backtesting, market analysis, risk monitoring, and optional live trade execution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure cryptocurrency trading analysis, backtest strategies, generate trading workflow guidance, and prepare configuration or command-oriented instructions for exchange-connected tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live cryptocurrency trades and exchange-connected workflows that may affect real funds.

Mitigation: Use paper trading or read-only analysis by default, and require explicit user confirmation before any real-money order.

Risk: Exchange API secrets may be needed for live trading workflows.

Mitigation: Use environment variables or a secrets manager, disable withdrawals on API keys, apply least-privilege permissions, and avoid exposing secrets in chat or logs.

Risk: The server security review marked the release as suspicious because high-risk live-trading actions are not clearly limited or warned about.

Mitigation: Review the skill before installation and add clear operational safeguards for live trading, credential handling, and order approval.

## Reference(s):

- [ClawHub skill page: trade-bot](https://clawhub.ai/thcjp/skills/trade-bot)
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with structured examples and inline JSON or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy parameters, backtesting inputs, execution checks, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
