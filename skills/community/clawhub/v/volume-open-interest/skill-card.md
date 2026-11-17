## Description:

Guides agents to use trading volume and open interest as corroborating evidence for price signals, trend health, blowoffs, selling climaxes, and COT interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, analysts, and agents assisting with market-analysis questions use this skill to evaluate whether trading volume and open interest confirm price signals, identify weak breakouts or crowded positions, and explain COT-related signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat educational volume and open-interest analysis as standalone financial advice.

Mitigation: Frame outputs as educational analysis, require independent validation, and avoid making trade recommendations without broader market context.

Risk: The artifact is mostly Chinese, which may be unsuitable for users expecting another language.

Mitigation: Honor the user's preferred language when stated and translate market-analysis terms clearly when responding in another language.

Risk: Volume and open-interest signals can be misleading when used without price context, seasonal adjustment, or futures-market data caveats.

Mitigation: Apply the skill's price-first posture, check total market volume and open interest where relevant, and call out limitations such as contract rollover, delayed settlement data, and crowded-position risk.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/bianchunhui/murphy-ta-skills/tree/main/volume-open-interest)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/volume-open-interest)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text]

**Output Format:** [Markdown or plain-text analytical guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational market-analysis guidance; no shell commands, configuration, or code generation are expected.]

## Skill Version(s):

0.1.0 (source: release evidence and test-prompts.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
