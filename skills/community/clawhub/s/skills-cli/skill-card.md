## Description:

High-level helper for managing agent skills with the ClawHub CLI and local skill folders across search, install, update, publish, and organization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to choose ClawHub CLI commands and local skill-directory workflows for searching, installing, updating, publishing, syncing, and checking skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publish and sync command suggestions can send local skill contents to ClawHub, including private prompts, secrets, or proprietary files if the target folder is not reviewed first.

Mitigation: Review the target skill folder, remove sensitive files, and confirm the exact path before running publish or sync commands.

Risk: Command guidance may be applied from the wrong working directory or to the wrong skill slug.

Mitigation: Confirm the workspace root, local skill path, slug, and intended version before executing generated ClawHub CLI commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/skills-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/openlang-cn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command selection and verification guidance; it does not describe automatic command execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
