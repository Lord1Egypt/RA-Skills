## Description:

Cloudflare R2 Storage management for setup, upload, download, listing, sync, and deletion through rclone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwatu](https://clawhub.ai/user/junwatu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure rclone for Cloudflare R2 and perform common object-storage operations such as upload, download, list, sync, and delete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may install rclone with a privileged curl-to-shell command.

Mitigation: Install rclone through a trusted package manager or a verified upstream release before running the skill.

Risk: R2 access keys are stored in local configuration files and can be displayed by the credential helper.

Mitigation: Use least-privilege, bucket-scoped R2 tokens; restrict permissions on ~/.config/r2/config.json and ~/.config/rclone/rclone.conf; avoid displaying credentials unless necessary.

Risk: Delete, purge, and sync delete operations can remove bucket data.

Mitigation: Preview target paths and bucket names carefully before destructive operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/junwatu/skills/r2-storage)
- [Publisher Profile](https://clawhub.ai/user/junwatu)
- [rclone Install Script](https://rclone.org/install.sh)
- [Cloudflare Dashboard](https://dash.cloudflare.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rclone-oriented setup and object-storage command guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
