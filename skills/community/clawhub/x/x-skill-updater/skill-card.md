## Description:

Checks OpenClaw skills for updates, supports weekly scheduled or manual checks, and notifies the user before running an upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snlcc](https://clawhub.ai/user/snlcc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to scan installed skills, compare local metadata against SkillHub or ClawHub registry data, review generated update reports, and run approved skill upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can inspect installed OpenClaw skills and trigger remote updates through external registries.

Mitigation: Install only in trusted OpenClaw environments and review configured sources, publishers, versions, and changelogs before accepting an update.

Risk: Bulk update mode can install multiple remote skill updates in one run without an enforced integrity check.

Mitigation: Prefer per-skill updates for normal use; reserve --all for reviewed source configurations and scan updated skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snlcc/skills/x-skill-updater)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local update reports and source-tracking JSON files when its scripts are run.]

## Skill Version(s):

1.2.0 (source: server release metadata; frontmatter lists v1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
