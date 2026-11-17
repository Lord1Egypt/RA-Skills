## Description:

Draws I Ching hexagrams using coins, time, or numbers through QiyueAstro, then displays the hexagram name, judgment text, line texts, changing lines, changed hexagram, and optional limited AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draw or browse I Ching hexagrams, show source hexagram text, and optionally request a limited QiyueAstro AI interpretation when the user explicitly asks for one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: I Ching requests and AI interpretation prompts are sent to QiyueAstro and, for interpretation, may be processed by an external AI service.

Mitigation: Tell users before interpretation calls that their question will be sent externally and advise them not to include highly sensitive personal information.

Risk: Divination and AI interpretation outputs could be mistaken for high-stakes advice.

Mitigation: Present the output as entertainment and self-exploration only, and do not rely on it for medical, legal, financial, safety, or other high-stakes decisions.

Risk: Skill outputs include promotional QiyueAstro links with tracking parameters.

Mitigation: Keep the destination visible to users so they can decide whether to follow the external link.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bloodymarygg/skills/qiyue-iching-drawer)
- [QiyueAstro Homepage](https://qiyueastro.com)
- [QiyueAstro I Ching API](https://qiyueastro.com/api/v1/openclaw/iching)
- [QiyueAstro Interpretation API](https://qiyueastro.com/api/v1/openclaw/interpret)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown with linked hexagram images, original hexagram text, and optional API-provided interpretation Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include QiyueAstro links and should preserve API-returned hexagram and interpretation text without model-authored reinterpretation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
