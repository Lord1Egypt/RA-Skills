## Description:

Triggers the publishing flow for existing local skills without creating new skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoulincom](https://clawhub.ai/user/zhoulincom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to publish one named local skill or all changed local skills through the repository publishing script. It is intended for release operations on existing skills, not for creating or editing skill content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented with simulated-upload wording but can perform real publishing operations for one or multiple skills.

Mitigation: Verify the target skill name or changed-skill list, registry, credentials, and publish script before running; avoid batch publishing unless all changed skills are intended for release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhoulincom/skills/simulated-upload-helper)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report publishing success, command failure details, or troubleshooting guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
