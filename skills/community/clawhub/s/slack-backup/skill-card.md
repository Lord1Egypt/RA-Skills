## Description: <br>
Backs up files uploaded to a Slack channel into the local ~/.openclaw/doc/backup directory with filters for count, filename, file type, and upload time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caigang78](https://clawhub.ai/user/caigang78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve real files from a Slack channel and persist verified backups locally. It is useful when a user needs recent Slack uploads saved by recency, name, type, or count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy potentially sensitive Slack files to a persistent local backup folder. <br>
Mitigation: Confirm the Slack token, workspace, and channel before use, and apply appropriate access controls and retention practices to ~/.openclaw/doc/backup. <br>
Risk: The submitted artifact depends on shared Slack helper files that were not included for review. <br>
Mitigation: Review the referenced shared helper files before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caigang78/slack-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Shell command execution that emits SUCCESS or ERROR status lines and writes downloaded files to a local backup directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables such as LIMIT, NAME_PREFIX, NAME_CONTAINS, MINUTES, FILE_TYPE, and BACKUP_DIR to select Slack files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
