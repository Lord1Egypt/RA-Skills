## Description:

OpenClaw skill for Zalo Bot API workflows (bot token) plus optional guidance on unofficial personal automation tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to plan Zalo Bot API workflows, token setup, webhook or polling delivery, messaging behavior, and operational guardrails. It also separates unofficial personal-account automation guidance so users can evaluate that path with explicit risk awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot tokens, webhook secrets, state files, and cookies can expose accounts or conversations if logged, committed, exported, or stored insecurely.

Mitigation: Store secrets in a secret manager, credentials store, or protected environment variables; avoid logging them; rotate compromised tokens; and keep development and production credentials separate.

Risk: Webhook and polling workflows can process duplicate, spoofed, or retried events incorrectly.

Mitigation: Validate webhook secrets, respond quickly, process work asynchronously, de-duplicate by message or event ID, and make handlers idempotent.

Risk: Unofficial personal-account automation uses cookies or session state and may violate platform terms or lead to account restrictions.

Mitigation: Prefer official bot APIs, use unofficial personal automation only for explicit low-risk workflows with user consent, avoid shared hosts, and protect or rotate session material.

Risk: Conversation context and profile metadata can retain more user information than the workflow needs.

Mitigation: Limit profile and context retention to the minimum required for the workflow and apply explicit allowlists for automation flows.

## Reference(s):

- [Bot Messaging Capabilities](references/zalo-bot-messaging-capabilities.md)
- [Zalo Bot Platform Overview](references/zalo-bot-overview.md)
- [Bot Token and Setup](references/zalo-bot-token-and-setup.md)
- [Bot UX Playbook](references/zalo-bot-ux-playbook.md)
- [Webhook and Polling Routing](references/zalo-bot-webhook-routing.md)
- [n8n Automation Notes](references/zalo-n8n-automation.md)
- [Personal Zalo Automation](references/zalo-personal-zca-js.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with workflow plans, checklists, and operational guardrails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration names for bot tokens, webhook secrets, webhook paths, polling cursors, and delivery policies.]

## Skill Version(s):

1.0.1 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
