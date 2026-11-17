## Description:

Calculate RSI for any asset. Use when checking overbought/oversold conditions, spotting divergence signals, comparing multi-timeframe RSI, or setting trading entry/exit alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill as an RSI reference aid for interpreting RSI zones, divergence patterns, and common trading-strategy concepts. It should not be treated as an asset-data calculator or trading advisor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its trading-analysis capabilities and present buy/sell labels that users could mistake for financial advice.

Mitigation: Use it only as an educational RSI reference and require independent financial analysis before making trading decisions.

Risk: The calculate command has a command-injection flaw when passed untrusted values.

Mitigation: Run the command only with trusted numeric period values, or review and patch input handling before deployment.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/rsi)
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style terminal text with command examples and RSI interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reference calculations, RSI zone labels, buy/sell/hold-style signals, divergence descriptions, and strategy notes.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
