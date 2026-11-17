## Description:

Build and operate a Quark/OpenList-style backup and restore workflow for OpenClaw workspaces, including QR login, account UID binding guard, whole-file cloud upload, dry-run restore, and manual Lighthouse snapshot policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliyunbot](https://clawhub.ai/user/aliyunbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, check, and operate account-guarded Quark cloud backups, restore dry runs, and manual snapshot workflows for OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes high-impact backup, cloud-upload, restore, and snapshot operations whose referenced helper scripts are not included for review.

Mitigation: Inspect and verify referenced script paths, ownership, permissions, and behavior before running upload, restore, cron, or snapshot commands.

Risk: Quark cookies, backup archives, restore indexes, and snapshot commands can expose sensitive account or recovery data.

Mitigation: Keep credentials and generated backup artifacts private, avoid logging secrets, run restore dry-runs first, and require explicit confirmation before snapshot creation or rollback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aliyunbot/skills/quarkpan-backup-suite)
- [Command Cookbook](references/commands.md)
- [Security Policy](references/security-policy.md)
- [Share This Skill](references/share.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
