## Description:

Sync the local Obsidian vault with a Cloudflare R2 bucket using rclone (S3 + crypt). Triggered by `/sync-notes`. Defaults to bidirectional sync; understands natural-language flags for partial download/upload by glob.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangsier-xyz](https://clawhub.ai/user/jiangsier-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and note-taking users use Sync Notes to configure and run encrypted bidirectional sync between a local Obsidian or Markdown vault and a Cloudflare R2 bucket. The agent translates `/sync-notes` requests into setup, status, baseline, full sync, upload, or download commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bidirectional sync can change or delete notes on both local and remote storage.

Mitigation: Run status and dry-run checks before first or broad syncs, resolve conflicts manually, and keep an independent backup of the vault.

Risk: R2 credentials and rclone crypt secrets are stored locally in configuration files.

Mitigation: Keep configuration files private with restrictive permissions, never expose secrets in chat, and back up the crypt passphrase offline.

Risk: Crafted shell configuration values or unrestricted extra rclone flags could cause unintended command execution or unsafe sync behavior.

Mitigation: Review generated configuration before syncing, validate setup inputs, and remove or allowlist extra rclone flags before deployment.

## Reference(s):

- [Sync Notes ClawHub Page](https://clawhub.ai/jiangsier-xyz/skills/sync-notes)
- [rclone Documentation](https://rclone.org/)
- [rclone Install Documentation](https://rclone.org/install/)
- [rclone Filtering Documentation](https://rclone.org/filtering/)
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [Remotely Save Obsidian Plugin](https://github.com/remotely-save/remotely-save)
- [Default rclone Filter Rules](config/filter.txt)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status or conflict summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local rclone configuration, logs, state, and backup files when its shell scripts are executed.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
