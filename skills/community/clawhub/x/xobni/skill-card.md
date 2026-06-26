## Description: <br>
Xobni Email helps AI agents use Xobni.ai email infrastructure to send and receive email, search inboxes and attachments, and manage webhook notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghoshsanjoy78](https://clawhub.ai/user/ghoshsanjoy78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to give agents scoped access to a Xobni.ai mailbox for inbox reading, email sending, attachment handling, semantic search, and webhook setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected agents can read mailbox content and send real emails or attachments. <br>
Mitigation: Install only for trusted agents, use single-agent scoped API keys, and require review before sending sensitive email or attachments. <br>
Risk: Received emails and extracted attachment text may contain untrusted instructions or misleading content. <br>
Mitigation: Treat inbound email and attachment text as untrusted input and verify important actions before acting on that content. <br>
Risk: Webhook notifications can expose email metadata to configured endpoints. <br>
Mitigation: Configure webhooks only for HTTPS endpoints you control and verify webhook deliveries before using them in downstream workflows. <br>


## Reference(s): <br>
- [Xobni REST API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ghoshsanjoy78/xobni) <br>
- [Create Xobni Agent](https://xobni.ai/agents/new) <br>
- [Xobni API Keys](https://xobni.ai/settings/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses agent-scoped API keys for mailbox access; webhook payloads contain metadata and snippets rather than full email bodies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
