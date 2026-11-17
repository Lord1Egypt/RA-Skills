## Description:

Full-featured X (Twitter) assistant for search, posting with media, threads, direct messages, Lists, bookmarks, trends, articles, block and mute actions, and related account workflows using Python standard library scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language X account tasks into reviewed shell commands for searching, reading, posting, messaging, media upload, list management, and account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise broad control over an X account, including posting, messaging, follows, blocks, mutes, bookmarks, Lists, and deletion workflows.

Mitigation: Use the least-privileged token possible, avoid sensitive accounts, and review every generated command before running it.

Risk: Many account-changing X actions can run without enforced confirmation, according to the authoritative security summary.

Mitigation: Require explicit human approval for write or destructive commands and verify the target account, post, message, or list before execution.

Risk: OAuth material may be cached in plaintext at ~/.x-helper/auth.json when the OAuth authorization flow is used.

Mitigation: Treat the token cache as a secret, restrict local access, prefer user-managed X_BEARER_TOKEN where possible, and remove cached OAuth material when no longer needed.

Risk: Tweet content, direct messages, media files, searches, user information, and bearer tokens are sent to X API services during normal use.

Mitigation: Do not use the skill with confidential content unless sharing it with X API services is acceptable.

## Reference(s):

- [X Helper on ClawHub](https://clawhub.ai/tobewin/skills/x-helper)
- [ToBeWin ClawHub profile](https://clawhub.ai/user/tobewin)
- [X Developer Portal](https://developer.x.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X_CLIENT_ID and X_BEARER_TOKEN for authenticated X API workflows.]

## Skill Version(s):

3.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
