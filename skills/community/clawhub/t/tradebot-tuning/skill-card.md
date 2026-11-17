## Description:

Adjust tradebot parameters incrementally to improve tradability based on market regime and diagnostic signals while maintaining risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[motivationationdaily](https://clawhub.ai/user/motivationationdaily)

### License/Terms of Use:


## Use Case:

Trading-bot operators and developers use this skill when a bot has stopped trading for long periods or diagnostics show persistent gate failures. It guides one-at-a-time parameter adjustments with verification after each change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parameter changes to a real-money trading bot can increase financial loss if applied without review or testing.

Mitigation: Keep daily loss caps and maximum trade limits enabled, test or paper trade before live use, and require explicit review before applying changes.

Risk: Multiple simultaneous tuning changes can make outcomes hard to attribute and can weaken safeguards.

Mitigation: Apply one change per cycle, log before and after values, and verify signal behavior after each adjustment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/motivationationdaily/skills/tradebot-tuning)
- [Publisher profile](https://clawhub.ai/user/motivationationdaily)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown guidance with parameter recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credential use, persistence, or hidden behavior identified by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
