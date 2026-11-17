## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainsakurawetc](https://clawhub.ai/user/rainsakurawetc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify relevant installable skills, compare options, and receive appropriate Skills CLI search or installation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend installing third-party agent skills globally while skipping confirmation.

Mitigation: Review the exact package, publisher, destination, and install command before use; avoid global installation and confirmation skipping unless necessary.

Risk: Unpinned third-party skill or CLI references may change between review and installation.

Mitigation: Prefer pinned CLI versions and immutable skill references, and scan selected skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rainsakurawetc/skills/t)
- [Skills CLI directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party skill recommendations and installation commands for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
