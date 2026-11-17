## Description:

Manage YouTube subscriptions by listing subscriptions or subscribers, subscribing to channels, and unsubscribing through the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage YouTube subscription workflows through the yutu CLI after configuring Google OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a YouTube account by inserting or deleting subscriptions.

Mitigation: Require explicit review and confirmation before running insert or delete commands, especially commands that delete multiple subscriptions.

Risk: The skill depends on a third-party CLI and sensitive OAuth credential and token files.

Mitigation: Verify the yutu package source and version before installation, and protect client_secret.json, youtube.token.json, YUTU_CREDENTIAL, and YUTU_CACHE_TOKEN values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openwaygate/skills/youtube-subscription)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [Yutu setup guide](references/setup.md)
- [Subscription delete reference](references/subscription-delete.md)
- [Subscription insert reference](references/subscription-insert.md)
- [Subscription list reference](references/subscription-list.md)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI flag tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local OAuth credential and token files required by yutu.]

## Skill Version(s):

0.10.7-dev (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
