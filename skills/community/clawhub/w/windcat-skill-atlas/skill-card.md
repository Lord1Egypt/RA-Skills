## Description:

Skill Atlas helps agents manage OpenClaw skills by guiding installation, updates, rollbacks, uninstall, backups, manifest tracking, security review, and loading-layer classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowenjiao54](https://clawhub.ai/user/guowenjiao54)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use Skill Atlas to organize OpenClaw skill inventories, choose install and update channels, manage backups and rollbacks, and decide whether skills should be core, resident, category, or paused.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to install, update, roll back, uninstall, and delete skills, which can change future agent behavior.

Mitigation: Use only when the publisher is trusted, and require visible user confirmation for batch restore, batch update, uninstall, rollback, and self-update operations.

Risk: Skill and backup file operations can affect unintended paths if slugs or paths are not constrained.

Mitigation: Validate skill slugs, reject path traversal, and keep file operations inside the managed skills and backups directories.

## Reference(s):

- [Skill Atlas ClawHub listing](https://clawhub.ai/guowenjiao54/skills/windcat-skill-atlas)
- [Skill Atlas detailed reference](artifact/reference.md)
- [Skill Atlas changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with code blocks, command templates, JSON examples, and concise agent response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes skill lifecycle procedures, manifest conventions, backup templates, channel selection rules, and safety review guidance.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter, evidence release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
