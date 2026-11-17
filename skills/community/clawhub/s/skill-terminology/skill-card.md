## Description:

Provides UML-related terminology aliases for agents, currently focused on sequence diagram terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to give an agent a compact UML terminology reference for recognizing sequence-diagram synonyms across multiple languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is loaded unconditionally and contains a mandatory instruction that may interfere with authorized edits to the skill files.

Mitigation: Review the skill before installation and use trusted skill-management workflows when updating, disabling, or removing it.

Risk: The always-loaded terminology content can influence agent behavior even when the current task is unrelated to UML terminology.

Mitigation: Install it only in workspaces where persistent UML terminology assistance is desired, and remove or disable it for unrelated workflows.

## Reference(s):

- [UML terminology reference](references/uml.md)
- [ClawHub skill page](https://clawhub.ai/lentiancn/skills/skill-terminology)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown terminology reference text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always-loaded terminology context; no executable output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
