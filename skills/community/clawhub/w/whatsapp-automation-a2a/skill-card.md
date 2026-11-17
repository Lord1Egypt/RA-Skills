## Description:

Automate WhatsApp outreach workflows for lead mining, bulk messaging, scheduled campaigns, AI-assisted replies, review collection, CRM pipeline tracking, and delivery analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-tradequo](https://clawhub.ai/user/alex-tradequo)

### License/Terms of Use:


## Use Case:

External business users, agencies, and developers use this skill to connect agents to MoltFlow's WhatsApp automation service for prospecting, campaign operations, customer follow-up, review capture, and CRM workflows. It is also useful for configuring Claude, ChatGPT, and MCP-based assistants to call MoltFlow APIs with user-controlled authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents messaging, scheduling, contact and group management, data export, document upload, and billing-affecting capabilities.

Mitigation: Use OAuth or short-lived least-privilege API keys, enable approval mode, and review any bulk, scheduled, AI-generated, or channel outbound messaging before execution.

Risk: Read-only onboarding workflows could be over-permissioned if paired with send or manage scopes.

Mitigation: Use read-only scopes for analysis workflows and reserve send, manage, export, and billing scopes for separately approved operational workflows.

Risk: Bulk or automated WhatsApp outreach can affect recipients at scale.

Mitigation: Configure phone whitelisting, require human approval for AI-generated content, and test campaigns with limited audiences before wider use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-tradequo/skills/whatsapp-automation-a2a)
- [MoltFlow homepage](https://molt.waiflow.app)
- [AI Agent Integrations](artifact/integrations.md)
- [Connect Claude to MoltFlow](https://molt.waiflow.app/guides/connect-claude-to-moltflow)
- [Connect ChatGPT to MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow)
- [MoltFlow Python SDK](https://github.com/moltflow/moltflow-python)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce outbound API call plans and setup instructions that require user-controlled credentials and approvals.]

## Skill Version(s):

2.16.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
