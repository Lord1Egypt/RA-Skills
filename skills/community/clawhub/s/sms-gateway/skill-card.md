## Description:

Send and receive SMS using a local sms-gate.app instance running on Android (via Termux) or a dedicated device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minstn](https://clawhub.ai/user/minstn)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to send SMS, check delivery status, inspect recent message history, and manage incoming SMS or delivery webhooks through a local Android sms-gate.app gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles SMS content and gateway credentials, and the security evidence flags weak network and webhook safeguards.

Mitigation: Use only a trusted HTTPS endpoint or protected local/VPN gateway, and restrict permissions on .env and .token.json.

Risk: Public webhook exposure can reveal incoming SMS payloads or forward them to an unintended endpoint.

Mitigation: Avoid public ngrok exposure unless additional authentication is in place, and disable or tightly control OPENCLAW_WEBHOOK_URL forwarding.

Risk: The provided scripts can send SMS, read message data, and modify webhook configuration.

Mitigation: Review requested actions before running scripts, use least-privilege gateway credentials where possible, and monitor webhook configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minstn/skills/sms-gateway)
- [SMS Gateway API Reference](references/api.md)
- [sms-gate.app](https://sms-gate.app)
- [Android SMS Gateway v1.55.0 release](https://github.com/capcom6/android-sms-gateway/releases/tag/v1.55.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger local API calls that send SMS, read message data, check gateway health, and manage webhook configuration when the agent runs the provided scripts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
