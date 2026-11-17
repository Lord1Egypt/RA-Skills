## Description:

Design, implement, and operate encrypted restic backups for Linux home directories with encryption, deduplication, automated scheduling, and restore testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiris-z](https://clawhub.ai/user/kiris-z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and workstation administrators use this skill to plan, install, validate, and operate encrypted restic backups for Linux home directories across system-level and user-level deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration handling can allow command execution through repository, hostname, email, path, retention, or timezone values when generated environment files are sourced by root-level or persistent timer jobs.

Mitigation: Review before installing, use only trusted literal values, inspect existing environment files before enabling timers, and prefer a fixed version that validates and escapes every generated configuration value.

## Reference(s):

- [Operator Runbook](references/runbook.md)
- [Ops Checklist](references/ops-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and file-path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged system changes, user-level systemd timers, restic repository operations, validation checks, and operational runbook steps.]

## Skill Version(s):

2.0.0 (source: server release metadata, artifact metadata, and SKILL.md contract)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
