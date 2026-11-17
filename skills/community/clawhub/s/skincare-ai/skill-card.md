## Description:

AISkinX Skincare AI Assistant is intended to analyze local skin images, provide skincare product recommendations, and answer skincare consultation questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[znsyhandao](https://clawhub.ai/user/znsyhandao)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers or agents supporting skincare workflows use this skill to turn local skin image inputs and skin-type details into analysis summaries, product recommendations, and consultation guidance. Treat the skincare analysis and advice as unverified informational guidance, not medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence rates the release as suspicious because safety and capability claims are stronger than the implementation.

Mitigation: Review the source before installation and treat the skincare outputs as mock or unverified unless the publisher provides a real analyzer and resolves the cited inconsistencies.

Risk: The skill handles local image paths and security evidence notes review-worthy file-validation gaps.

Mitigation: Use only non-sensitive images kept inside the skill directory or configured allowed folders, and run the skill in a sandboxed environment.

Risk: Skincare recommendations could be mistaken for medical or dermatological advice.

Mitigation: Present results as informational skincare guidance only and direct users to qualified professionals for medical skin concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/znsyhandao/skills/skincare-ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Text, Markdown, or JSON responses containing skin analysis summaries, recommendations, status details, and guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local-file validation messages and confidence-style skincare scoring; no verified clinical accuracy is established by the supplied evidence.]

## Skill Version(s):

1.0.4 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
