## Description:

Intercepts risky rm commands to assess impact, confirm user intent, and suggest safer alternatives before execution to prevent accidental data loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caesaryp](https://clawhub.ai/user/caesaryp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add an extra confirmation step before destructive file deletion commands, including impact assessment and safer alternatives such as trash, backup, or moving files to a temporary location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable latest/default-branch installation instructions can change the installed code over time.

Mitigation: Prefer a pinned ClawHub CLI version or a reviewed release or commit before installation.

Risk: A destructive delete command can still proceed if the user confirms without reviewing the target and impact assessment.

Mitigation: Review the resolved target path and deletion impact carefully, and prefer trash or backup options when recovery may be needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caesaryp/skills/rm-safety)
- [Publisher Profile](https://clawhub.ai/user/caesaryp)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown confirmation prompts with inline shell commands and structured safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese user-facing confirmation text.]

## Skill Version(s):

1.2.2 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
