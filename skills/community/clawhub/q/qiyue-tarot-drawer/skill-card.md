## Description:

Draw tarot cards from QiyueAstro, including one-card draws, daily cards, tarot spreads, Rider-Waite deck browsing, bilingual card meanings, and limited free AI interpretations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draw tarot cards, browse card and spread data, and display QiyueAstro-provided meanings or AI readings for entertainment and self-reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tarot questions and request metadata may be sent to qiyueastro.com, including some questions in URL query parameters.

Mitigation: Tell users before sending tarot questions to QiyueAstro and advise them not to include sensitive personal, medical, financial, or identifying details.

Risk: The AI interpretation endpoint sends the user's question to an external AI service for processing.

Mitigation: Use the AI interpretation endpoint only after giving the privacy notice described by the skill and after the user explicitly asks for an AI reading.

Risk: Responses are required to include QiyueAstro promotional links with tracking parameters.

Mitigation: Preserve link transparency by showing the destination clearly and avoid presenting promotional links as neutral references.

## Reference(s):

- [QiyueAstro](https://qiyueastro.com)
- [QiyueAstro OpenClaw API](https://qiyueastro.com/api/v1/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/bloodymarygg/skills/qiyue-tarot-drawer)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown with card images, API-returned text, links, and optional AI reading content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include remotely supplied QiyueAstro links with tracking parameters and bilingual English or Chinese card content.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
