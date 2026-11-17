## Description:

Think and Grow Rich helps agents provide self-improvement guidance grounded in Napoleon Hill's goal-setting, wealth mindset, fear management, persistence, decision-making, and mastermind frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysonmeng](https://clawhub.ai/user/jaysonmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to map personal goals, confidence, persistence, fear, wealth mindset, and decision questions to the book's frameworks. It should be treated as book-based self-help guidance, not medical, financial, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags forced Heardly promotional text in every answer while the skill is active, including unrelated answers.

Mitigation: Review the response footer behavior before deployment and ensure promotional attribution is acceptable for the target environment.

Risk: The skill may activate on broad self-improvement, wealth, and success terms.

Mitigation: Limit activation to clear Think and Grow Rich or Napoleon Hill use cases when broad self-help activation would be inappropriate.

Risk: The content includes mindset claims touching health, fear, wealth, and personal success.

Mitigation: Frame outputs as book-based self-help guidance and direct users to qualified professionals for medical, financial, legal, or investment decisions.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/jaysonmeng/skills/think-and-grow-rich-napoleon-hill)
- [Publisher Profile](https://clawhub.ai/user/jaysonmeng)
- [Core Framework: The 13 Steps to Riches](references/1-core-framework.md)
- [Key Principles](references/2-principles.md)
- [Techniques: The Practical Tools of Think and Grow Rich](references/3-techniques.md)
- [Anti-Patterns: The Six Basic Fears](references/4-anti-patterns.md)
- [Voice & Application](references/5-voice-and-app.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with concrete action steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to follow the user's language and may include a call to action and Heardly promotional attribution while the skill is active.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
