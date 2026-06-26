## Description: <br>
Send and receive SMS using a local sms-gate.app instance running on Android or a dedicated device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minstn](https://clawhub.ai/user/minstn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send SMS messages, check delivery status, inspect recent message history, run gateway health checks, and manage SMS webhooks through a local Android sms-gate.app instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real SMS messages from a connected device. <br>
Mitigation: Require manual approval before sending messages and keep credentials limited to trusted users and agents. <br>
Risk: Incoming SMS webhooks may expose message content or forward it beyond the local receiver. <br>
Mitigation: Avoid public exposure unless authentication and transport controls are in place, and set OPENCLAW_WEBHOOK_URL=disabled unless forwarding is intentional. <br>
Risk: Gateway credentials and cached tokens can grant access to SMS actions. <br>
Mitigation: Protect .env and .token.json, rotate credentials if exposed, and keep the gateway on a trusted network. <br>


## Reference(s): <br>
- [SMS Gateway API Reference](references/api.md) <br>
- [sms-gate.app](https://sms-gate.app) <br>
- [Android SMS Gateway v1.55.0 Release](https://github.com/capcom6/android-sms-gateway/releases/tag/v1.55.0) <br>
- [ClawHub Skill Page](https://clawhub.ai/minstn/sms-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMS_GATE_URL, SMS_GATE_USER, SMS_GATE_PASS, python3, an SMS-capable Android device, and a reachable sms-gate.app local server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
