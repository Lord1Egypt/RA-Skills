## Description: <br>
Helps agents work with the Resend email API for transactional email, inbound email webhooks, templates, delivery events, domains, contacts, broadcasts, webhooks, API keys, automations, logs, and SDK setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christina-de-martinez](https://clawhub.ai/user/christina-de-martinez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through Resend email workflows, including sending transactional emails, receiving inbound mail, configuring webhooks and domains, managing contacts and broadcasts, and handling API keys safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward production-impacting Resend actions such as sending emails or broadcasts, enabling automations, changing domains or webhooks, modifying contacts, or creating and deleting API keys. <br>
Mitigation: Require explicit user confirmation for those actions and review recipients, payloads, domains, webhook endpoints, automation state, and API-key scopes before execution. <br>
Risk: The skill requires sensitive Resend credentials and may involve webhook signing secrets. <br>
Mitigation: Store secrets only in environment variables, use least-privilege Resend API keys, avoid exposing tokens in logs or generated code, and rotate credentials if disclosure is suspected. <br>
Risk: Inbound email, logs, and attachments may contain untrusted or sensitive content. <br>
Mitigation: Verify webhook signatures, retrieve only the data needed for the task, redact sensitive content when sharing outputs, and apply additional inbox security controls before allowing automated downstream actions. <br>
Risk: Retries or malformed batch requests can duplicate or block email sends. <br>
Mitigation: Use idempotency keys for retryable sends, validate batch payloads before submission, and prefer single sends when attachments or scheduling are required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/christina-de-martinez/resend-skills) <br>
- [Resend Skill Documentation](https://resend.com/docs/resend-skill) <br>
- [Resend Skill Repository](https://github.com/resend/resend-skills) <br>
- [Resend Agent Skills](https://resend.com/agent-skills) <br>
- [Resend Documentation](https://resend.com/docs) <br>
- [Resend API Reference](https://resend.com/docs/api-reference) <br>
- [Sending Overview](references/sending/overview.md) <br>
- [Sending Best Practices](references/sending/best-practices.md) <br>
- [Receiving](references/receiving.md) <br>
- [Webhooks](references/webhooks.md) <br>
- [API Keys](references/api-keys.md) <br>
- [Automations](references/automations.md) <br>
- [Logs](references/logs.md) <br>
- [Installation](references/installation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include language-specific SDK examples and operational checklists for Resend workflows.] <br>

## Skill Version(s): <br>
3.3.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
