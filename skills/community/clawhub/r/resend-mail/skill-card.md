## Description: <br>
Manage Resend email campaigns, contacts, audiences, domains, templates, and transactional sends via the Resend API for inspection, audience management, email creation, sending, and workflow automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, email operators, and support teams use this skill in OpenClaw to inspect Resend activity, manage audiences and contacts, configure domains, templates, webhooks, and API keys, and send transactional or batch emails through a connected Resend account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a connected Resend account through ClawLink credentials, so actions can affect contacts, audiences, domains, templates, webhooks, API keys, and outbound email. <br>
Mitigation: Use a Resend account and permission level appropriate for the intended tasks, verify the connected integration before use, and review write previews carefully. <br>
Risk: Email sends, destructive changes, webhook updates, and API-key creation or revocation can have irreversible or broad operational effects. <br>
Mitigation: Require explicit confirmation for write actions, inspect the target resource and intended effect before execution, and prefer read or describe calls before changes. <br>


## Reference(s): <br>
- [Resend API Documentation](https://resend.com/docs/api-reference/introduction) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Dashboard](https://claw-link.dev/dashboard?add=resend) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/resend-mail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, discovery guidance, troubleshooting notes, and Resend tool-call examples; write actions require preview and explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
