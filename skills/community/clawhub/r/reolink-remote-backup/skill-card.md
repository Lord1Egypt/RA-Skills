## Description:

Sets up reliable off-site Reolink camera backup for remote cameras or constrained home networks using a VPS relay, FTP/FTPS ingest, local/NAS pull sync, retention, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccaprani](https://clawhub.ai/user/ccaprani)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and technically capable camera owners use this skill to design and operate an off-site backup path for Reolink cameras when direct camera-to-home ingest is impractical. It helps configure a VPS relay, local pull synchronization, retention cleanup, and troubleshooting for upload, authentication, path, and protocol failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes root-level VPS setup and persistence steps that can modify package, firewall, FTP service, user, SSL, and retention configuration.

Mitigation: Review the scripts before running them, back up existing vsftpd and UFW configuration, and run them only on the intended VPS.

Risk: Misconfigured retention or access controls could delete backups unexpectedly or broaden access to camera files.

Mitigation: Validate retention-days input, keep separate restricted users and dedicated SSH keys, prefer FTPS after debugging, and keep SSH command restrictions constrained.

## Reference(s):

- [Reolink Remote Backup Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/ccaprani/skills/reolink-remote-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and bundled Bash scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup scripts for VPS FTP/FTPS ingest, local rsync pull, a systemd user timer, retention cleanup, and troubleshooting.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
