## Description:

Manages skill distribution and visibility across AI agents using a two-layer, two-dimension Universal Skill Manager with syncing and scope control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hulk-yin](https://clawhub.ai/user/hulk-yin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep local skills synchronized across multiple agent platforms, manage visibility scopes, provision skill metadata, and audit which agents can access each skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change multiple agent skill directories.

Mitigation: Use dry-run modes first, inspect agents.yaml and each meta.yaml scope, and review proposed changes before running synchronization.

Risk: The migration script can delete conflicting local skill folders without a real backup.

Mitigation: Back up ~/.skills and agent skill folders yourself, and avoid running migration on directories containing local or uncommitted skill work until conflict handling is improved.

## Reference(s):

- [Skill Manager on ClawHub](https://clawhub.ai/hulk-yin/skills/skill-manager-usm)
- [Provisioning Specialist Agent](artifact/agents/provision_agent.md)
- [ClawHub Distribution](artifact/references/clawhub_distribution.md)
- [meta.yaml Schema](artifact/references/meta_schema.md)
- [Skill Naming Conflict Resolution](artifact/references/naming_conflict.md)
- [skill-creator](https://github.com/ZiweiAxis/skill-creator)
- [skill-installer](https://github.com/ZiweiAxis/skill-installer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that alter skill metadata, symlinks, and agent skill directories; dry-run modes are available for bundled synchronization and migration scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
