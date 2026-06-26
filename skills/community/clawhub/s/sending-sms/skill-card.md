## Description: <br>
Sends SMS messages via the Sendly API with the Node.js SDK or REST API. Handles single messages, batch sends, scheduling, conversations, and sandbox testing. Applies when sending text messages, notifications, alerts, or reminders via SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sendly-live](https://clawhub.ai/user/sendly-live) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use this skill to send transactional or marketing SMS messages, schedule reminders, perform batch sends, and test Sendly integrations in sandbox mode before live delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Sendly API keys can send real SMS messages and incur charges. <br>
Mitigation: Use sandbox keys first, and confirm recipient numbers, message content, message type, and expected charges before any live send. <br>
Risk: Marketing or batch messages can create consent, compliance, and quiet-hours risk. <br>
Mitigation: Confirm consent and compliance status before sending, especially for marketing, scheduled, or batch messages. <br>
Risk: Sendly API keys could be exposed through prompts, logs, or shared files. <br>
Mitigation: Keep the API key in environment variables and out of prompts, logs, and shared files. <br>


## Reference(s): <br>
- [Sendly SMS API Docs](https://sendly.live/docs/sms) <br>
- [Sendly SDK Docs](https://sendly.live/docs/sdks) <br>
- [Sendly OpenAPI Spec](https://sendly.live/openapi.yaml) <br>
- [Sendly Sandbox Docs](https://sendly.live/docs/sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include live API calls that send SMS messages, consume credits, or schedule future delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
