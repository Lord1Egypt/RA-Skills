## Description: <br>
Complete WhatsApp Business Cloud API for messages, templates, media, webhooks, flows, and business profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to work with WhatsApp Business Cloud API messaging, templates, media, webhooks, flows, and business profile operations. It helps draft requests, configuration guidance, webhook handling patterns, and operational checks for business messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help operate a real WhatsApp Business messaging account, including customer messages and account changes. <br>
Mitigation: Require explicit user confirmation before sending customer messages, deleting resources, updating business profiles, or changing two-step verification. <br>
Risk: Meta access tokens, app secrets, webhook verification tokens, and customer message data are sensitive. <br>
Mitigation: Keep secrets out of chat and memory files; use environment variables or a secrets manager and avoid logging message content. <br>
Risk: Saved local account context may contain phone numbers, webhook URLs, or business configuration details. <br>
Mitigation: Review any local memory before reuse or sharing and store only the minimum operational context needed. <br>
Risk: Unverified webhook requests could lead to spoofed events or incorrect automated responses. <br>
Mitigation: Verify webhook signatures with the Meta app secret before processing inbound events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/whatsapp-business-api) <br>
- [Skill homepage](https://clawic.com/skills/whatsapp-business-api) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Messages guide](artifact/messages.md) <br>
- [Templates guide](artifact/templates.md) <br>
- [Webhooks guide](artifact/webhooks.md) <br>
- [Best practices guide](artifact/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, JSON, JavaScript, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, webhook handling snippets, and configuration checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
