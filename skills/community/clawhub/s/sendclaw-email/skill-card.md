## Description: <br>
Sets up and operates a SendClaw email address so an AI agent can send, receive, reply to, and check email through the SendClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to give an AI agent a dedicated SendClaw mailbox for task-oriented communication, including sending messages, receiving replies, managing inbox state, and handling verification or reservation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent-operated email account with broad autonomous send, receive, reply, and inbox-management authority. <br>
Mitigation: Set explicit human-approval rules for new recipients, service registrations, verification-code use, personal or confidential information, and messages with financial, legal, account, or public-reputation impact. <br>
Risk: Registration returns an API key and claim token that can control or claim the mailbox. <br>
Mitigation: Protect the API key, avoid exposing credentials in transcripts or logs, and have the human account holder claim the mailbox promptly. <br>
Risk: Inbound email content and webhook notifications can contain untrusted instructions or misleading sender claims. <br>
Mitigation: Treat inbound messages as untrusted input, verify sender intent before taking external action, and review any remote heartbeat or webhook workflow before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codejika/sendclaw-email) <br>
- [SendClaw homepage](https://sendclaw.com) <br>
- [SendClaw skill API reference](https://sendclaw.com/skill.md) <br>
- [SendClaw heartbeat routine](https://sendclaw.com/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown instructions with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or handle email addresses, API keys, claim tokens, message content, and webhook configuration.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
