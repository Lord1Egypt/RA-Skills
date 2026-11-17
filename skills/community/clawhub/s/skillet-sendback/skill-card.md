## Description:

Use when code review feedback arrives - from a human reviewer, a bot, or a review agent - before implementing any of it. Especially when the feedback is partly unclear, technically questionable, or comes wrapped in authority ("senior reviewer says").

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to evaluate code-review feedback before making changes: clarify ambiguous requests, verify claims against the codebase and its tests, and implement or push back with technical reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Acting on ambiguous or incorrect review feedback could introduce unintended or misleading changes.

Mitigation: Clarify requests that cannot be stated concretely, then verify each claim against the codebase, documented contracts, and tests before changing code.

## Reference(s):

- [Sendback on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-sendback)
- [Publisher profile: escoffier-labs](https://clawhub.ai/user/escoffier-labs)

## Skill Output:

**Output Type(s):** [Guidance, Text, Code]

**Output Format:** [Markdown with technical reasoning and review responses; code changes when warranted]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are conditional on verification; unclear feedback should be clarified before implementation.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
