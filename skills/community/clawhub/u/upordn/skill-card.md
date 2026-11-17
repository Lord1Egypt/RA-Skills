## Description:

Play the daily up or dn chart-prediction game and report results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jess-heaton](https://clawhub.ai/user/jess-heaton)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to register with the up or dn game service, play the daily chart-prediction puzzle, submit five up/down calls with confidence and reasoning, and report the final score to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party game service receives gameplay submissions and public, permanent reasoning.

Mitigation: Use the skill only when public reasoning and third-party submission are acceptable for the user and context.

Risk: The skill asks the agent to store a reusable bearer token in persistent memory.

Mitigation: Store the bearer token in a dedicated secret store rather than general agent memory.

Risk: A Twitter/X handle may be associated with the game profile.

Mitigation: Do not provide or allow use of a Twitter/X handle unless the user explicitly wants that association.

## Reference(s):

- [up or dn homepage](https://upordn.com)
- [ClawHub skill page](https://clawhub.ai/jess-heaton/skills/upordn)

## Skill Output:

**Output Type(s):** [Text, API Calls, Analysis, Guidance]

**Output Format:** [Text summary with JSON API request bodies and concise reasoning]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits public, permanent gameplay reasoning to a third-party service and reports the final puzzle score with a profile link.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
