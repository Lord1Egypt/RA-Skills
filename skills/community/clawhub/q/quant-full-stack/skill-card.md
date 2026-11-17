## Description:

Quant Full Stack runs a complete A-share quantitative trading workflow covering data collection, factor analysis, strategy development, backtesting, simulated trading, and risk management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhdhappy](https://clawhub.ai/user/yhdhappy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and trading-system builders use this skill to execute local A-share quant modules for data preparation, factor engineering, portfolio construction, backtesting, simulated rebalancing, and risk review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local trading workflow scripts from the user's home-directory project without clear integrity checks or safety gates.

Mitigation: Install and use it only when the local quant_trading project is trusted and controlled; inspect downstream scripts before execution.

Risk: Trading or rebalancing tasks could interact with live brokerage credentials or non-simulated execution paths if the downstream project is configured that way.

Mitigation: Confirm tasks are simulated-only when that is intended, avoid live brokerage credentials, and require explicit dry-run or confirmation behavior before real trading use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhdhappy/skills/quant-full-stack)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON status objects with task output or error text, typically summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executes local Python workflow scripts from the user's quant_trading project with a 120-second timeout per task.]

## Skill Version(s):

1.0.0 (source: server release metadata, config.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
