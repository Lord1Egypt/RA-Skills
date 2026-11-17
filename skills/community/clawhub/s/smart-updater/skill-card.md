## Description:

Smart Updater helps OpenClaw users inventory installed skills, extensions, and core packages, scan for updates, review changelogs and risk, and execute only user-approved upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanhui](https://clawhub.ai/user/yuanhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Smart Updater to check installed assets, identify available updates across npm, ClawHub, and GitHub sources, review changelog-driven risk summaries, and apply only explicitly approved upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsigned remote package downloads or tampered local metadata could overwrite OpenClaw assets during installation or upgrade.

Mitigation: Require signature or digest verification before replacing installed assets, and canonicalize install paths under approved OpenClaw roots before deletion or copy operations.

Risk: Upgrade scripts can modify local skills, extensions, and core assets.

Mitigation: Keep upgrade execution behind explicit user confirmation, review generated inventory and scan results, and retain rollback backups before applying changes.

## Reference(s):

- [Smart Updater ClawHub Page](https://clawhub.ai/yuanhui/skills/smart-updater)
- [OpenClaw](https://openclaw.ai)
- [Three Gates Reference](references/three-gates.md)
- [Report Format](references/report-format.md)
- [Product Requirements](docs/PRD.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports with JSON inventory and scan files plus shell command execution output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires inventory and scan results before final reporting; upgrade execution waits for explicit user approval.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata; changelog dated 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
