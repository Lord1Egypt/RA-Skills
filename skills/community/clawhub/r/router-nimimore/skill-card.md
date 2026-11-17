## Description:

Automatically selects an AI model for a query by analyzing query characteristics and balancing cost against expected task complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aichiafranco](https://clawhub.ai/user/aichiafranco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to select a cost-appropriate model tier for simple, code, reasoning, Chinese-language, and long-context queries. It can return routing analysis and selected model metadata for use in CLI workflows or agent orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downstream use of the selected model could send prompt content to Moonshot or Bailian providers.

Mitigation: Review selected provider names before sending sensitive prompts, and treat the skill as a local routing helper rather than a complete model gateway.

## Reference(s):

- [Router NIMIMORE ClawHub listing](https://clawhub.ai/aichiafranco/skills/router-nimimore)
- [Publisher profile](https://clawhub.ai/user/aichiafranco)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON objects and concise routing guidance, with optional CLI command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes query feature flags, selected model name, model tier, token-cost metadata, and estimated savings.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
