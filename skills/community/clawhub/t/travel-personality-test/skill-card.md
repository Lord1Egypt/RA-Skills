## Description:

Runs a 10-question travel personality quiz and returns a personality card with destination recommendations based on the user's answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwhite-qi](https://clawhub.ai/user/gwhite-qi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travelers use this skill to explore their current travel style through a lightweight quiz and receive personality-aligned destination suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and invoke the unpinned external FlyAI dependency for live recommendations, sending travel preferences, destinations, dates, or budget details to an external service.

Mitigation: Review and approve the FlyAI dependency path before installation or use, and share sensitive travel details only when an external lookup is intended.

Risk: Live destination trends, flight prices, and hotel prices may be unavailable, rate limited, or unsuitable for the user's context.

Mitigation: Use the bundled city reference pool as a fallback and clearly label fallback recommendations as reference-based when FlyAI calls fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwhite-qi/skills/travel-personality-test)
- [FlyAI skill integration guide](https://github.com/alibaba-flyai/flyai-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation responses with quiz prompts, personality cards, destination recommendations, and occasional shell command snippets for FlyAI setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request or use travel preferences, destinations, dates, and budget details when producing recommendations.]

## Skill Version(s):

1.1.0 (source: server release metadata and target metadata; artifact docs mention 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
