## Description:

Adds random, non-repeating Chinese title labels to assistant replies to make responses feel more personalized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowaa223](https://clawhub.ai/user/guowaa223)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to decorate assistant responses with a selected Chinese title label and optional emoji. It is suited to casual or branded interactions where a consistent reply prefix is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reply decoration can change exact response formatting in workflows that require strict output shape.

Mitigation: Avoid enabling the skill for exact-format tasks, or disable the title prefix in those workflows.

Risk: The skill keeps local title-use history in history.json so titles do not repeat.

Mitigation: Review or reset the local history file when persistent title state is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowaa223/skills/title-replier)
- [Publisher profile](https://clawhub.ai/user/guowaa223)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Text or markdown-style assistant reply prefix, with optional CLI text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepends a randomly selected Chinese title label, optionally with an emoji, and records used labels in local history.json to reduce repeats.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
