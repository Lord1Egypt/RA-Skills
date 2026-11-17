## Description:

Helps coding agents turn vague aesthetic and outcome-driven requests into scoped, runnable code through a confirmed Vibe Lock and incremental delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to clarify feel, outcome, exclusions, and stack before building a first runnable slice from an ambiguous prototype request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The clarification checkpoint may interrupt already well-specified development requests.

Mitigation: Use the skill for vague prototype requests; correct the Vibe Lock or follow the normal implementation flow when the specification is precise.

Risk: Vague requests can still lead to incorrect dependencies or unintended features in generated code.

Mitigation: Confirm scope and stack, verify dependencies, and test each runnable slice before expanding the feature set.

## Reference(s):

- [Vibe Code release](https://clawhub.ai/jhauga/skills/vibe-code)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A four-line Vibe Lock precedes code; implementation proceeds one runnable slice at a time.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
