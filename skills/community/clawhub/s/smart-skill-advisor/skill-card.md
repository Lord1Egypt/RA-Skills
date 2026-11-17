## Description:

Turn a user goal into the best skill stack. Recommends, compares, and sequences the right skills, with explicit user approval before any install guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, builders, and teams use this skill to translate a goal into a small ClawHub skill stack, compare alternatives, and sequence a safer workflow before installing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended skills may carry trust, setup, or third-party install risks if the user later adopts them.

Mitigation: Review each recommended skill's trust signals and setup requirements, and require explicit approval before any install guidance.

Risk: A recommended stack can be mismatched when available skill signals are incomplete or low quality.

Mitigation: Compare alternatives, explain tradeoffs and confidence, and prefer the smallest effective stack.

## Reference(s):

- [Smart Skill Advisor on ClawHub](https://clawhub.ai/tobewin/skills/smart-skill-advisor)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown with structured recommendation, execution plan, alternatives, tradeoff, and gated install guidance sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Install guidance is only provided after explicit user approval; recommendations include risk and setup notes.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
