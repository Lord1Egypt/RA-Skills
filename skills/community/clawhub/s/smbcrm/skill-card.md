## Description:

Provides SMBcrm-focused guidance for Private Integration Tokens, REST API v2, workflows, custom webhooks, MCP, Agent Studio API, troubleshooting, automation design, data sync, and AI assistant setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[section5media](https://clawhub.ai/user/section5media)

### License/Terms of Use:

MIT-0

## Use Case:

SMBcrm customers, operators, developers, and integration teams use this skill to design, troubleshoot, and implement advanced CRM automations, API integrations, webhooks, MCP clients, and Agent Studio API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Integration Tokens can grant broad access to SMBcrm data and actions.

Mitigation: Use least-privilege scopes, separate tokens by environment, store tokens in a secret manager, avoid logging token values, and rotate tokens regularly.

Risk: Generated API, workflow, or curl examples may modify CRM records, payments, invoices, public posts, or bulk contact data.

Mitigation: Review proposed commands and payloads before execution, test with sandbox or staging tokens first, and confirm rollback steps for write workflows.

Risk: Webhook and MCP integrations can expose sensitive customer data or trigger unintended side effects.

Mitigation: Use HTTPS, shared-secret verification, idempotency keys, narrow agent instructions, and read-only tokens where write access is not required.

## Reference(s):

- [SMBcrm API documentation](https://developers.smbcrm.com/)
- [SMBcrm ClawHub skill page](https://clawhub.ai/section5media/skills/smbcrm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline JSON, HTTP, shell, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
