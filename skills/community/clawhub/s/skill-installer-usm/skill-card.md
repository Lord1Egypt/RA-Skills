## Description:

Install, search, update, and manage skills from public registries like ClawHub using the clawhub CLI within the OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hulk-yin](https://clawhub.ai/user/hulk-yin)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and operators use this skill to search, install, update, and inspect OpenClaw skills from public registries, then coordinate installed skills with the local USM hub and agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update third-party skills and thereby change available agent capabilities.

Mitigation: Review the requested skill slug, registry, and target paths before installation or update, and require explicit approval for untrusted requests.

Risk: Chat- or shell-triggered installation requests may be ambiguous or come from untrusted messages.

Mitigation: Confirm the exact command intent with the user and prefer a pinned or verified clawhub CLI version before changing installed skills.

## Reference(s):

- [Skill Installer ClawHub Listing](https://clawhub.ai/hulk-yin/skills/skill-installer-usm)
- [ClawHub Registry](https://clawhub.ai)
- [Skill Manager Repository](https://github.com/ZiweiAxis/skill-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request user confirmation before installing CLI dependencies or enabling third-party skills.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
