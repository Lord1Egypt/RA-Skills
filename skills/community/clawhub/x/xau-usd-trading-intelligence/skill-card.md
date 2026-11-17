## Description:

Use when analyzing XAU/USD with data-driven market regimes, multi-timeframe structure, liquidity, momentum, volatility, macro context, risk management, trade journaling, and continuous learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill for XAU/USD decision-support analysis, including market regime review, multi-timeframe structure, liquidity, momentum, macro context, risk management, scenario planning, and trade journaling. It is intended to support analysis and documentation, not to guarantee trading outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the skill's analysis for an automated trading system or guaranteed financial advice.

Mitigation: Treat outputs as decision support only, verify current market data, and make independent risk decisions before trading.

Risk: Trade journal notes may include sensitive account, strategy, or personal information if users provide it.

Mitigation: Avoid entering private account details unless necessary, and redact sensitive information before storing journal notes locally.

Risk: Stale or unavailable market data can make live XAU/USD analysis unreliable.

Mitigation: Require timestamped data sources for current analysis and lower confidence or choose no-trade when data quality is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/xau-usd-trading-intelligence)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [multi_tf_checklist.py](artifact/scripts/multi_tf_checklist.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with structured checklists and optional plain-text CLI checklist output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are decision-support artifacts and should be reviewed against current market data before use.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
