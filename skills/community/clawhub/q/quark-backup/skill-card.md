## Description:

quark-backup helps agents back up an OpenClaw .openclaw directory to Quark Netdisk, either manually or through a daily 04:00 cron job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z157181773](https://clawhub.ai/user/z157181773)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure and run backups of OpenClaw workspace, memory, sessions, and configuration data to Quark Netdisk. It supports one-time backups, scheduled cron backups, upload verification, and restore guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup may upload broad private OpenClaw state to Quark Drive.

Mitigation: Review backup contents before use, narrow the archive where possible, and encrypt archives that may contain sensitive workspace, memory, session, or configuration data.

Risk: The workflow depends on a full Quark session cookie.

Mitigation: Store the cookie with strict file permissions or a secret manager, avoid including it in backup archives, and rotate it if exposure is suspected.

Risk: Scheduled cron execution can repeatedly run the backup before the kuake binary source is verified.

Mitigation: Pin and verify the kuake binary source before enabling cron, then monitor backup logs and upload verification results.

## Reference(s):

- [kuake CLI setup reference](references/kuake-setup.md)
- [Quark Netdisk](https://pan.quark.cn)
- [ClawHub skill page](https://clawhub.ai/z157181773/skills/quark-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to configure a Quark Cookie secret, run backup shell scripts, or schedule cron execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
