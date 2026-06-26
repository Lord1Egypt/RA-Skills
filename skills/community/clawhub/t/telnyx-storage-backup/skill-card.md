## Description: <br>
Backup and restore your OpenClaw workspace to Telnyx Storage. Simple CLI-based scripts with no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to back up, list, and restore OpenClaw workspace files with Telnyx Storage. It supports custom buckets, workspace paths, backup retention, and cron-compatible recurring backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace backups may contain sensitive OpenClaw data or secrets and are uploaded to Telnyx Storage. <br>
Mitigation: Use a private bucket, least-privileged Telnyx credentials, and review backed-up files for secrets before recurring uploads. <br>
Risk: Retention settings can delete older backup archives. <br>
Mitigation: Choose MAX_BACKUPS intentionally and test retention behavior before enabling scheduled backups. <br>
Risk: Restoring a backup can overwrite local workspace files. <br>
Mitigation: Restore only from backups you trust and confirm the target workspace before extraction. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teamtelnyx/telnyx-storage-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include commands for backup, listing, restore, retention, and scheduling workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
