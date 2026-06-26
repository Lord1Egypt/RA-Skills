## Description: <br>
Robotomail gives an AI agent a real inbox and outbound email for sending, reading, replying to, and reacting to messages through the Robotomail API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnjoubert](https://clawhub.ai/user/johnjoubert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect agents to Robotomail mailboxes for support inboxes, outbound follow-ups, reminders, replies, and real-time inbound email workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can read, send, and monitor real email through Robotomail. <br>
Mitigation: Install only when real email access is intended, use a scoped API key where possible, and confirm every send and mailbox read. <br>
Risk: Webhook and SSE setup can create persistent email monitoring flows. <br>
Mitigation: Avoid all-mailbox webhooks unless required, limit events and mailboxes to the workflow, and review persistent monitoring setup before enabling it. <br>
Risk: The skill requires a sensitive Robotomail API key. <br>
Mitigation: Store ROBOTOMAIL_API_KEY as a secret, rotate or revoke keys when no longer needed, and prefer mailbox-scoped keys when supported. <br>


## Reference(s): <br>
- [Robotomail ClawHub Skill Page](https://clawhub.ai/johnjoubert/robotomail) <br>
- [Robotomail Website](https://robotomail.com) <br>
- [Robotomail API Reference](artifact/references/api-reference.md) <br>
- [Webhook Signature Verification](artifact/references/webhook-verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with HTTP endpoint guidance, JSON examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Robotomail API key supplied through ROBOTOMAIL_API_KEY.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
