## Description:

Sends WeCom group robot webhook notifications as text, Markdown, Markdown V2, image, or file messages, either to a supplied webhook URL or to a registered named chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinyao](https://clawhub.ai/user/gavinyao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send service alerts, scheduled job results, data reports, and other notifications to WeCom chats from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs can grant message-sending access and may be exposed by registry listings or shared logs.

Mitigation: Treat webhook URLs as secrets, avoid sharing listing output, and restrict permissions on the local registry file.

Risk: User-provided messages or files can be sent to arbitrary webhook URLs.

Mitigation: Prefer pre-registered trusted destinations and review command arguments before sending content or files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gavinyao/skills/qywx-msg-sender)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts send user-selected text, Markdown, images, and files to WeCom webhook endpoints and maintain an optional local chat registry.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
