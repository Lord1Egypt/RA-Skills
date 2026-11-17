## Description:

在微信 Mac 版发送消息。当用户提到"微信发消息"、"发微信"、"给 XXX 发微信"时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvin-dean](https://clawhub.ai/user/calvin-dean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to guide an agent through WeChat for Mac UI automation that searches for a contact and sends a message from the logged-in account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send a WeChat message immediately to the first matched search result, including an unintended recipient.

Mitigation: Require visible confirmation of the exact resolved contact and message before sending, and avoid partial-name top-result selection.

Risk: User-provided contact or message text may be interpolated into shell or AppleScript automation commands.

Mitigation: Pass contact and message text as data, escape inputs correctly, and avoid constructing executable script source from raw user text.

Risk: The skill controls the logged-in user's WeChat Mac UI and can send messages through that account.

Mitigation: Install and run only when the user accepts agent control of WeChat, and keep local UI automation permissions limited to the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvin-dean/skills/wechat-send-message)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell, AppleScript, and UI automation command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local WeChat for Mac session and UI automation permissions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
