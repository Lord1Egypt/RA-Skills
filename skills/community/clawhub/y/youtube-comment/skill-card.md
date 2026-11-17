## Description:

Manage YouTube comments by listing, creating, updating, deleting, marking as spam, or setting moderation status through the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage YouTube comment workflows from an agent by preparing yutu commands for listing replies, creating or updating comments, deleting comments, and applying moderation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party yutu CLI that receives Google or YouTube OAuth credentials.

Mitigation: Use a pinned and verified yutu version, keep client_secret.json and youtube.token.json out of repositories and shared workspaces, and restrict access to credential files.

Risk: Comment deletion, spam marking, rejection, and author bans can change public YouTube content or account moderation state.

Mitigation: Manually review comment IDs, target channels, and moderation statuses before executing commands, especially destructive or bulk actions.

## Reference(s):

- [Yutu CLI homepage](https://github.com/eat-pray-ai/yutu)
- [ClawHub skill page](https://clawhub.ai/openwaygate/skills/youtube-comment)
- [Setup guide](references/setup.md)
- [Comment list reference](references/comment-list.md)
- [Comment insert reference](references/comment-insert.md)
- [Comment update reference](references/comment-update.md)
- [Comment delete reference](references/comment-delete.md)
- [Comment mark-as-spam reference](references/comment-markAsSpam.md)
- [Comment moderation-status reference](references/comment-setModerationStatus.md)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can return table, JSON, YAML, or silent output depending on yutu flags.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
