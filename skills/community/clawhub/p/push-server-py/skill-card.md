## Description:

Send notifications to WeCom users through a configurable OpenAPI push service, supporting TEXT, MARKDOWN, TEXT_CARD, and NEWS message types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[es-v](https://clawhub.ai/user/es-v)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send operational WeCom notifications from an agent workflow through a configured push server. It supports plain text, markdown, card, and news-style notification payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured Push Server URL receives the API key and notification contents.

Mitigation: Use only a controlled, trusted HTTPS push server and treat QYWX_PUSH_API_KEY as a credential capable of sending messages.

Risk: Notification payloads may be exposed because the script prints full request content to stdout.

Mitigation: Avoid sending secrets or regulated data through this skill unless logging is changed to redact sensitive content.

## Reference(s):

- [Push Server](https://github.com/qingzhou-dev/push-server)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/es-v/skills/push-server-py)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Python command output containing a JSON success response or plain-text error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus QYWX_PUSH_API_KEY and QYWX_PUSH_URL environment variables.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
