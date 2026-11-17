## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krislavten](https://clawhub.ai/user/krislavten)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to find relevant reskill ecosystem skills, review registry results, and install selected skills into supported agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search public registries and install other skills, which may persistently change agent behavior.

Mitigation: Install it only when this behavior is intended, review the exact skill publisher, version, and registry before approval, and scan skills before deployment.

Risk: The documented fallback can use unpinned remote package execution through npx reskill@latest.

Mitigation: Prefer a locally reviewed and pinned reskill installation, and avoid running npm, npx, or reskill with elevated privileges.

## Reference(s):

- [reskill package manager](https://github.com/nicepkg/reskill)
- [Rush community registry](https://rush.zhenguanyu.com/)
- [ClawHub skill page](https://clawhub.ai/krislavten/skills/rush-find-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose registry searches and installations; user approval is expected before installing skills.]

## Skill Version(s):

0.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
