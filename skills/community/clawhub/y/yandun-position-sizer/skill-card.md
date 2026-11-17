## Description:

Yandun Position Sizer produces educational demonstration position-sizing, stop-loss, take-profit, and risk-budget outputs from supplied stock codes and capital.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate teaching examples for position size, stop-loss, take-profit, and portfolio risk exposure calculations. Outputs should be treated as educational demonstrations and not as investment or trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake educational demonstration output for real investment or trading advice.

Mitigation: Label outputs as demonstrations and state that they are not investment advice before presenting calculated positions, stop-losses, or take-profit values.

Risk: Built-in prices and deterministic risk scores may be stale or unrelated to current market conditions.

Mitigation: Require independently verified live market data and qualified review before using any similar calculation in a real financial decision.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/caoling7878-arch/skills/yandun-position-sizer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from a Python CLI, typically summarized by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses deterministic built-in demonstration prices and risk rules; no live market data.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
