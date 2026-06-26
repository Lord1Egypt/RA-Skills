## Description: <br>
Build and operate a Quark/OpenList-style backup and restore workflow for OpenClaw workspaces, including QR login, account UID binding guard, whole-file cloud upload, dry-run restore, and manual Lighthouse snapshot policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliyunbot](https://clawhub.ai/user/aliyunbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to set up Quark Drive backups, validate restore procedures, guard account binding, and manage manual Lighthouse snapshot rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups, checksums, cookies, and cloud links can expose sensitive workspace or account information. <br>
Mitigation: Treat these files and credentials as sensitive, avoid logging Quark cookies, auth keys, preview URLs, or share tokens, and remove local secrets before sharing the skill. <br>
Risk: Cloud uploads can be sent to the wrong Quark account if account binding is not checked. <br>
Mitigation: Run the account binding guard before cloud writes and block uploads on UID mismatch. <br>
Risk: Restore and snapshot rollback commands can overwrite current state. <br>
Mitigation: Run restore dry-runs first, keep rollback checkpoints, and require explicit confirmation before snapshot creation or rollback. <br>


## Reference(s): <br>
- [QuarkPan Backup Suite on ClawHub](https://clawhub.ai/aliyunbot/quarkpan-backup-suite) <br>
- [Command Cookbook](references/commands.md) <br>
- [Security Policy](references/security-policy.md) <br>
- [Share This Skill](references/share.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and configuration checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preflight checks, account-guard steps, dry-run restore guidance, manual snapshot actions, and sharing instructions.] <br>

## Skill Version(s): <br>
0.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
