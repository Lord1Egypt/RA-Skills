## Description:

Design, implement, and operate encrypted restic backups for Linux home directories with systemd automation, retention policies, and restore validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moep90](https://clawhub.ai/user/moep90)

### License/Terms of Use:


## Use Case:

Developers, operators, and Linux users use this skill to set up encrypted restic backups for home directories, including scheduling, retention, integrity checks, and restore validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The privileged bootstrap can turn crafted setup values into root shell execution.

Mitigation: Review or patch the bootstrap before installing, and do not run it with --apply, --init-repo, or --enable-timers unless repository, password-file, username, and timezone inputs are trusted and safely escaped.

Risk: Generated restic environment files and systemd units may apply sensitive backup configuration with elevated privileges.

Mitigation: Verify /etc/restic-home.env and generated systemd units before enabling timers or running an initial backup.

## Reference(s):

- [Restic Home Backup Ops Checklist](artifact/references/ops-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/moep90/skills/restic-home-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, file paths, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate restic setup artifacts, systemd service and timer definitions, validation steps, and an operator runbook.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
