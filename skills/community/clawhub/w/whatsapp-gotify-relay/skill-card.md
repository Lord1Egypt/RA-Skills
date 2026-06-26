## Description: <br>
Use when operating or extending this WhatsApp Gotify relay as the bridge to OpenClaw. Prefer Unix tools for Docker, logs, Gotify queue checks, webhook validation, and relay smoke tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jr551](https://clawhub.ai/user/jr551) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run, test, and maintain a WhatsApp-to-OpenClaw relay that uses Gotify queues and webhooks for outbound messages, inbound events, and connection status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gotify, webhook, and WhatsApp credentials are sensitive and could expose relay control or message data if mishandled. <br>
Mitigation: Store tokens as secrets, avoid logging them, and confirm all environment variables point only to systems you operate. <br>
Risk: Manual outbox curl commands can send real WhatsApp messages. <br>
Mitigation: Run manual send commands only against an intended relay and recipient, and review the JSON payload before execution. <br>
Risk: Unfiltered WhatsApp protocol or history-sync events can create noisy or misleading inbound webhook traffic. <br>
Mitigation: Forward only meaningful conversation events and keep Gotify and webhook payload contracts lean and aligned. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jr551/whatsapp-gotify-relay) <br>
- [Project homepage](https://github.com/jr551/gotify-whatsapp-queue) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on relay operations, environment variables, payload contracts, Docker commands, Gotify queue checks, webhook validation, and smoke tests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
