## Description:

Skill Install Guard intercepts skill installation requests, runs a skill-vetter security review, reports the result, and requires explicit user confirmation before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongyulin89](https://clawhub.ai/user/dongyulin89)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add a security review checkpoint before installing or updating skills from ClawHub, URLs, or local sources. It is intended to produce a safety report and require explicit approval before any install command runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill can still authorize installation from vague confirmations such as continue or OK.

Mitigation: Require an explicit confirmation phrase that names the exact skill being installed, especially for URL installs, updates, or failed reviews.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongyulin89/skills/skill-install-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown safety review report with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before installation commands are executed.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
