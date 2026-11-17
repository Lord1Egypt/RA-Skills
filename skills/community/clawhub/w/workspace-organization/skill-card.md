## Description:

Automates OpenClaw workspace health checks and setup guidance by detecting broken symlinks, empty directories, large files, malformed names, disk usage, file counts, recent changes, and Git status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to initialize standard workspace structure, run periodic workspace audits, and review cleanup recommendations before backups, deployments, or maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs can expose local workspace paths, recent activity, and repository state.

Mitigation: Keep audit logs local or sanitize them before sharing.

Risk: The setup script can replace existing notes, docs, or scripts README files in the target workspace.

Mitigation: Run setup only in a fresh or backed-up workspace, or review the target files before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/skills/workspace-organization)
- [Publisher profile](https://clawhub.ai/user/donovanpankratz-del)
- [Installation and setup guide](artifact/README.md)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and local audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Bash scripts for workspace setup and audit reporting; no API keys or credential environment variables were detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
