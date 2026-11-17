## Description:

This skill helps an agent search for a WeChat friend, confirm the intended recipient, and send a text message through a configured WeChat bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aw11100](https://clawhub.ai/user/aw11100)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to let an agent find a WeChat contact and send a text message after recipient confirmation. It is intended for messaging workflows backed by a configured WeChat bridge service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured private-network endpoint or WECHAT_APPID could point to an unintended WeChat bridge.

Mitigation: Confirm the endpoint and WECHAT_APPID before installation or use.

Risk: A message could be sent to the wrong contact if a friend search returns multiple or ambiguous matches.

Mitigation: Use the required recipient selection and confirmation step before calling the sendText action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aw11100/skills/wechatmessaging)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown or plain text with API-backed tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires recipient lookup and user confirmation before sending a message.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
