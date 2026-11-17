## Description:

Draws Meihua Yishu divination results through QiyueAstro's public API, supporting time-based or number-based casting and optional free AI interpretation without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to cast Meihua Yishu hexagrams for entertainment and self-exploration questions, then display the returned hexagram text, changing lines, and related QiyueAstro links. When users explicitly request AI interpretation, the skill can call QiyueAstro's interpretation service after warning that the question will be processed by an external AI service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions may be sent to qiyueastro.com and, for interpretation, processed by an external AI service.

Mitigation: Warn users before calling the interpretation endpoint and advise them not to include highly sensitive personal, financial, medical, or relationship details.

Risk: Outputs include external QiyueAstro promotional links with tracking parameters.

Mitigation: Present the final link as an external promotional link and avoid implying NVIDIA ownership or endorsement.

Risk: Divination and AI interpretation can be mistaken for factual, professional, or decision-grade advice.

Mitigation: Frame results as entertainment and self-exploration, preserve API-returned text, and avoid adding model-authored conclusions outside the documented interpretation flow.

## Reference(s):

- [QiyueAstro](https://qiyueastro.com)
- [QiyueAstro Meihua Open API](https://qiyueastro.com/api/v1/openclaw/meihua)
- [ClawHub Skill Page](https://clawhub.ai/bloodymarygg/skills/qiyue-meihua-drawer)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown with returned API text, image links, and optional interpretation markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include QiyueAstro promotional links with tracking parameters and should preserve API-returned divination text without model-authored interpretation unless the interpretation endpoint is used.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
