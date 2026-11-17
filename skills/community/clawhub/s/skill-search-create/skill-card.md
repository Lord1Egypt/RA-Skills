## Description:

Searches ClawHub for existing skills and helps create a new OpenClaw skill when no suitable match is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[condamnation](https://clawhub.ai/user/condamnation)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search ClawHub for reusable skills, create an OpenClaw skill structure when no match exists, and prepare a skill for publication through the ClawHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or relying on the ClawHub CLI package introduces dependency trust and version-control considerations.

Mitigation: Confirm the package source is trusted before installation and prefer pinned or reviewed dependency versions in managed environments.

Risk: Publishing a skill can upload code and metadata to an external service.

Mitigation: Review generated skill files and metadata before running publish commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/condamnation/skills/skill-search-create)
- [ClawHub](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and skill-structure guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose ClawHub CLI search, create, login, and publish commands.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
