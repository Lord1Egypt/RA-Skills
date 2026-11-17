## Description:

Trading Execution helps agents produce market-monitoring workflows, Upbit trading automation commands, portfolio allocation guidance, scheduled trading tasks, and safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation users use this skill to draft operational workflows for market monitoring, Upbit trading automation, portfolio allocation, scheduled checks, and safety guardrails before any live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trading guidance can affect real funds if applied directly to live exchange accounts.

Mitigation: Confirm referenced trading scripts, start with backtesting or paper trading, require explicit confirmation for live orders, and set budget and loss limits.

Risk: Exchange API keys can enable unauthorized or unintended trades if over-scoped or poorly stored.

Mitigation: Use narrowly scoped exchange API keys and store them securely before connecting any live account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cooperiano/skills/trading-execution)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; outputs should be reviewed before live trading use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
