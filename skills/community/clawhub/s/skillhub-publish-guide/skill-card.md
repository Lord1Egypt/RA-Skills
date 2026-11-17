## Description:

Provides an agent-facing publishing guide for preparing and publishing skills to SkillHub.cn while separating publishable packages from runtime credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawhub-master](https://clawhub.ai/user/clawhub-master)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a checklist and command reference for packaging, publishing, and verifying SkillHub.cn skill releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded real-looking tokens and API keys can cause credential compromise if reused or copied into another release.

Mitigation: Do not install or use the skill as published; rotate exposed credentials and replace all credential values with placeholders before release.

Risk: The artifact directs agents toward external login, publishing, memory access, and document upload actions.

Mitigation: Require explicit user approval before any external login, publish, upload, or memory-access action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawhub-master/skills/skillhub-publish-guide)
- [SkillHub.cn registry](https://skill.xfyun.cn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with shell command blocks, configuration examples, and checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires credential replacement and explicit approval before any external login, publishing, upload, or memory-access action.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
