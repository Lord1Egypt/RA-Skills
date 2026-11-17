## Description:

Provides predictions with quantified uncertainty by evaluating data completeness, prediction type, and confidence to inform decision-making risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keys-li](https://clawhub.ai/user/keys-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to assess uncertainty when making predictions, judgments, or recommendations. It helps surface confidence level, information completeness, prediction type, and when further verification is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidence scores can be mistaken for guarantees of correctness, especially for speculative or low-information predictions.

Mitigation: Treat scores as advisory, state the source of uncertainty, and verify important decisions against authoritative sources.

Risk: The skill may activate broadly around predictions or judgments, which can add cautionary output where it is not needed.

Mitigation: Apply it when uncertainty assessment is useful and keep outputs concise for routine low-risk responses.

Risk: The artifact instructions are primarily Chinese-language, which can make review harder for teams that do not read Chinese.

Mitigation: Have a qualified reviewer confirm the behavior and prompts before deployment.

## Reference(s):

- [Skill reference standards](artifact/references/standards.md)
- [Skill usage guide](artifact/assets/guide.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Code]

**Output Format:** [Markdown or structured text with confidence scores, uncertainty notices, and risk levels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a 0-10 confidence score, information completeness label, prediction type, and risk warning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
