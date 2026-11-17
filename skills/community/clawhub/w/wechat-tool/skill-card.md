## Description:

The wechat-tool skill helps an agent search WeChat friends, recent contacts, chatrooms, and chatroom members, then send text, image, or file messages after target confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aw11100](https://clawhub.ai/user/aw11100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to manage WeChat lookup and messaging workflows through an agent, including finding the intended recipient, confirming the target, and sending text, image, or file content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account tokens, recipient details, contact identifiers, messages, and file URLs may be sent to a third-party service over plain HTTP.

Mitigation: Install only if the service is trusted, prefer HTTPS with certificate validation, store WECHAT_TOKEN in a secrets manager, and rotate any token previously used over HTTP.

Risk: The skill can send text, image, and file messages to friends or groups.

Mitigation: Keep the target lookup, user selection for multiple matches, and second confirmation step before every send action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aw11100/skills/wechat-tool)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Markdown with tool call parameters and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WECHAT_APPID and WECHAT_TOKEN configuration before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
