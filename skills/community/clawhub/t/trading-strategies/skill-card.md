## Description:

Comprehensive trading knowledge base covering fundamentals, technicals, strategies, backtesting, and risk management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill as a trading research and system-design reference for strategy evaluation, backtesting, technical indicators, and risk management. Outputs should be treated as informational support rather than financial advice or authorization to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading guidance can be mistaken for financial advice or treated as an instruction to execute live trades.

Mitigation: Require human review for trading decisions and treat skill output as informational research support only.

Risk: Agent-built trading systems may introduce financial loss through unvalidated strategies, overfitting, or incorrect market assumptions.

Mitigation: Use paper trading, out-of-sample backtesting, explicit limits, and compliance review before any live deployment.

Risk: Broker or exchange API keys could enable unwanted live trading if connected without controls.

Mitigation: Use withdrawal-disabled keys, explicit trade approvals, position and loss limits, and separate implementation review before connecting broker or exchange APIs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rmbell09-lang/skills/trading-strategies)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with possible code, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational trading research and system-design support; does not include executable code in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
