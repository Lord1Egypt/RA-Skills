## Description: <br>
Backup OpenClaw state directory and workspace. Includes excluding sensitive files, packaging for backup. Triggered when user asks to backup, export, or save state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HackSing](https://clawhub.ai/user/HackSing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create local backups of OpenClaw state and workspace files, then store or transfer the resulting archive for migration or recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain sensitive OpenClaw state or workspace files even though common credential, key, log, and cache patterns are excluded. <br>
Mitigation: Confirm the source directories, inspect archive contents before sharing, encrypt backups stored outside the local machine, and delete unencrypted local copies after storage or transfer. <br>
Risk: Remote storage examples can expose private workspace data if used with a public or untrusted destination. <br>
Mitigation: Use only private destinations, verify that secrets and private workspace files are excluded or encrypted, and avoid remote sync examples until the destination is reviewed. <br>


## Reference(s): <br>
- [Skill source: SKILL.md](artifact/SKILL.md) <br>
- [Backup script](artifact/scripts/backup.sh) <br>
- [ClawHub skill page](https://clawhub.ai/HackSing/safe-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline bash commands; the backup script creates a gzip-compressed tar archive.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENCLAW_STATE_DIR and OPENCLAW_WORKSPACE_DIR when set; otherwise defaults to the user's OpenClaw state and workspace directories.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
