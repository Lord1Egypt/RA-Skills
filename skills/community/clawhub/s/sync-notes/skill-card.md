## Description: <br>
Sync Notes helps an agent synchronize a local Obsidian or Markdown notes vault with a Cloudflare R2 bucket using rclone, encrypted S3 storage, and rclone crypt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangsier-xyz](https://clawhub.ai/user/jiangsier-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-taking users use this skill to configure and run encrypted synchronization between a local notes folder and a Cloudflare R2 bucket. It supports first-time setup, baseline initialization, routine bidirectional sync, status checks, and targeted uploads or downloads by glob. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routine synchronization can modify or delete notes on both the local filesystem and the Cloudflare R2 bucket. <br>
Mitigation: Use status checks and dry runs during initial setup, establish the baseline deliberately, and review conflict output before running another sync. <br>
Risk: Cloudflare R2 credentials and crypt settings are written to local skill configuration files. <br>
Mitigation: Use a narrowly scoped R2 token, keep generated configuration files out of commits and backups, and preserve the crypt passphrase securely outside the synced notes folder. <br>
Risk: Local backups are rolling snapshots and may be overwritten by later write-side operations. <br>
Mitigation: Create a manual backup before large deletes, schema changes, or other high-impact sync operations. <br>


## Reference(s): <br>
- [ClawHub Sync Notes listing](https://clawhub.ai/jiangsier-xyz/sync-notes) <br>
- [rclone documentation](https://rclone.org/) <br>
- [rclone install documentation](https://rclone.org/install/) <br>
- [Cloudflare R2 documentation](https://developers.cloudflare.com/r2/) <br>
- [Remotely Save Obsidian plugin](https://github.com/remotely-save/remotely-save) <br>
- [rclone filtering documentation](https://rclone.org/filtering/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, rclone, CLOUD_NOTES_PATH, and user-supplied Cloudflare R2 and crypt credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
