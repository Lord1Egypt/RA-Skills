## Description:

Pre-trade safety checks: position size limits, leverage validation, consecutive loss locks, volatility gates, exchange balance verification. Drop-in risk guard for any trading skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill as a pre-trade gate that checks position sizing, leverage, consecutive losses, volatility, and available exchange balance before a trading agent proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a cryptocurrency payment address and Telegram activation path for a claimed pro trading execution feature.

Mitigation: Do not send cryptocurrency or use the Telegram activation path; review any trading execution feature separately through trusted platform channels before installation or use.

Risk: Trading risk checks can be incomplete or misleading if treated as a guarantee of trade safety.

Mitigation: Use the skill only as a pre-trade checklist and keep independent controls for capital limits, leverage, exchange balances, and volatility thresholds.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sg345662365-oss/skills/trade-safety-vetter)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with checklist thresholds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, tool calls, or configuration files are included in the artifact.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
