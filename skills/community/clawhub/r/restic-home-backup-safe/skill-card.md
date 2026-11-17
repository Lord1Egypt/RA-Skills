## Description:

Design, implement, and operate encrypted restic backups for Linux home directories with systemd automation, retention policies, and restore validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moep90](https://clawhub.ai/user/moep90)

### License/Terms of Use:


## Use Case:

Developers, engineers, and Linux operators use this skill to plan and apply encrypted restic backups for home directories, including systemd schedules, retention, integrity checks, and restore validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe configuration handling in the root-level setup script could lead to command execution as root.

Mitigation: Use plan mode only until inputs are validated and safely quoted, configuration is not sourced as shell code, and the script has been reviewed before any root execution.

Risk: Credential files or generated systemd services may be installed with insufficient hardening.

Mitigation: Require restrictive credential permissions from creation time, verify generated paths before applying, and add least-privilege systemd settings before enabling timers.

## Reference(s):

- [Restic Home Backup Ops Checklist](references/ops-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, generated script/configuration paths, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plan-only setup steps by default; system changes require explicit apply confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
