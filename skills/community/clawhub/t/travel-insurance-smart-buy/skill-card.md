## Description:

旅行保险智能推荐与理赔指南，提供场景化保险推荐、条款白话解读和理赔流程指引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to compare travel insurance coverage, understand policy terms in plain language, and prepare claim steps for common travel scenarios. The output is informational and should be checked against insurer terms before purchase or claim submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares PROXY_TOKEN while also claiming that it needs no API key and does not transmit user data.

Mitigation: Require the publisher to explain or remove PROXY_TOKEN before installation and confirm whether trip details can pass through any proxy or external service.

Risk: Travel insurance recommendations and claim guidance can be incomplete or different from the insurer's binding policy terms.

Mitigation: Treat output as informational and verify coverage, exclusions, claim deadlines, and required documents with the insurer or official policy before acting.

Risk: The included Python tool file may not run because of syntax errors.

Mitigation: Fix and test the tool file before deployment, or use the skill only as static guidance until the executable artifact is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/travel-insurance-smart-buy)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown-style text recommendations and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include insurance coverage suggestions, plain-language term explanations, claim document checklists, and purchase-channel links.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
