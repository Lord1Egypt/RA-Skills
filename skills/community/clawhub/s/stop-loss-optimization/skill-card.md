## Description:

用动态止损锁定利润，避免"小盈大亏"。用于A股风控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-focused agents use this skill as an informational framework for A-share stop-loss and trailing stop decisions. It helps structure cost-line, profit-protection, and extreme-market exit guidance without authorizing account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to provide firm stop-loss or sell-order style trading instructions.

Mitigation: Use the skill only as an informational framework and require explicit human review and confirmation before any trade or account action.

Risk: The guidance does not define broader suitability, portfolio-risk, or financial-advice boundaries.

Mitigation: Present outputs as general risk-management guidance and apply independent financial, legal, and user-specific review before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haohanyang92/skills/stop-loss-optimization)
- [Publisher profile](https://clawhub.ai/user/haohanyang92)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational trading-risk guidance only; no account actions should be taken without explicit human review and confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
