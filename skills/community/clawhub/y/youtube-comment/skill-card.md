## Description: <br>
Manage YouTube comments by listing, creating, updating, deleting, marking as spam, and changing moderation status through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, channel operators, and agents use this skill to manage YouTube comment workflows from the command line after configuring Google OAuth credentials and yutu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credential and cached token files can grant access to a YouTube account. <br>
Mitigation: Keep client_secret.json, youtube.token.json, YUTU_CREDENTIAL, and YUTU_CACHE_TOKEN out of source control and chats; restrict access to the local environment where yutu runs. <br>
Risk: Delete, reject, spam, ban-author, update, and insert commands can modify live YouTube comments. <br>
Mitigation: Verify comment IDs, target status, author-ban settings, and comment text before allowing the agent to run mutating commands. <br>


## Reference(s): <br>
- [Yutu CLI Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Setup Guide](references/setup.md) <br>
- [Comment Delete](references/comment-delete.md) <br>
- [Comment Insert](references/comment-insert.md) <br>
- [Comment List](references/comment-list.md) <br>
- [Comment MarkAsSpam](references/comment-markAsSpam.md) <br>
- [Comment SetModerationStatus](references/comment-setModerationStatus.md) <br>
- [Comment Update](references/comment-update.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands, option tables, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through yutu and can require OAuth credential and token configuration.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
