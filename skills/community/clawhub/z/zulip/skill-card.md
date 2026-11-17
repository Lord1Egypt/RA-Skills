## Description:

Interact with Zulip chat platform via REST API and Python client. Use when you need to read messages from streams/topics, send messages to channels or users, manage DM conversations, list users, or integrate with Zulip organizations for team communication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suky57](https://clawhub.ai/user/suky57)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect an agent to a Zulip organization through a bot account, read stream or direct messages, send replies, list users, and share files for team communication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private messages, send direct messages, post to streams, and upload files through the configured Zulip bot.

Mitigation: Use a least-privilege bot account and require confirmation before reading private messages, sending messages, posting to streams, or uploading files.

Risk: Zulip bot API credentials can be exposed through source control, shell history, or shared logs.

Mitigation: Keep zuliprc out of source control, restrict its file permissions, and avoid pasting real API keys into shell commands or shared logs.

## Reference(s):

- [Zulip API Quick Reference](references/api-quick-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, curl, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Zulip API reads, message sends, and file uploads through a configured bot account.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
