## Description:

WeChat Operate helps an agent find WeChat friends, recent contacts, group chats, and group members, confirm the target, and send text, image, or file messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aw11100](https://clawhub.ai/user/aw11100)

### License/Terms of Use:

MIT-0

## Use Case:

External users or developers use this skill to manage WeChat contacts and send confirmed text, image, or file messages through a trusted local WeChat bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive WeChat contact and message operations are routed over an unencrypted local HTTP endpoint.

Mitigation: Install only with a trusted local WeChat bridge and network; prefer HTTPS and authentication before using sensitive contacts, message text, images, files, or file URLs.

Risk: Messages, images, or files could be sent to the wrong recipient if the target is ambiguous.

Mitigation: Search for the target first, show choices when multiple matches are returned, and require explicit confirmation before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aw11100/skills/wechat-operate)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, Files, Guidance]

**Output Format:** [Plain text or Markdown confirmations plus HTTP requests to the WeChat bridge]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires recipient lookup and explicit user confirmation before sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
