## Description: <br>
Provides AI agents with @claw.inc email addresses to send, receive, and securely communicate with humans and other AI agents via email and API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travisvz](https://clawhub.ai/user/travisvz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building AI agents use Sky to provision an agent email address, send outbound messages, receive inbound email through webhooks or polling, and support agent-to-agent communication over @claw.inc addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sky handles email content and metadata for the agent. <br>
Mitigation: Use a dedicated account and API key, minimize sensitive data in messages, and install only when the publisher and service are trusted. <br>
Risk: API keys and webhook secrets could be exposed through logs, commits, or agent output. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid printing real keys, and rotate credentials if exposure is suspected. <br>
Risk: Inbound email or cron-polled messages could steer the agent toward unsafe actions. <br>
Mitigation: Verify webhook signatures, require approval for important outbound messages, and constrain automated message processors so inbound content cannot directly control the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travisvz/sky) <br>
- [Sky security documentation](https://sky.ai/security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, HTTP, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint examples, webhook payload formats, rate-limit notes, and operational best practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
