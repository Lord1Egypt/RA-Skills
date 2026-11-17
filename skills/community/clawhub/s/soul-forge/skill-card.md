## Description:

SoulForge analyzes local session history and SOUL.md to surface behavioral patterns, propose reviewed updates, and help keep an agent profile aligned with the user's observed preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taha2053](https://clawhub.ai/user/taha2053)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use SoulForge to observe local session patterns, generate reflection reports, and review proposed changes to SOUL.md before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SoulForge can create a persistent behavioral profile from local session history.

Mitigation: Review before installing, disable automatic observation if passive tracking is not desired, and inspect local observation storage during setup.

Risk: Proposed SOUL.md changes may encode incorrect or unwanted inferences about the user.

Mitigation: Review every proposed diff before applying changes and avoid auto-accept for profile updates.

Risk: The security review notes that documented storage boundaries may not match the shipped file layout.

Mitigation: Verify where observations and backups are written in the installed environment before regular use.

## Reference(s):

- [SoulForge ClawHub page](https://clawhub.ai/taha2053/skills/soul-forge)
- [Declared project homepage](https://github.com/Taha2053/soulforge)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, proposed diffs, and interactive CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local observation memory and can update SOUL.md only after approval; dry-run and status modes produce review-only output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
