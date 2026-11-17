## Description:

Connect your agent to Zoho CRM via MCP to search contacts, list accounts, query records with COQL, and manage CRM data using mcporter with paginated, custom-field-aware helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintcx](https://clawhub.ai/user/sprintcx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to connect an agent to Zoho CRM, inspect contacts and accounts, run COQL queries, and prepare controlled CRM read or write workflows through a configured MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Zoho MCP URL contains CRM access credentials and can expose customer data if logged, screenshotted, or stored carelessly.

Mitigation: Treat ZOHO_MCP_URL as a secret, avoid echoing it, prefer per-session storage where practical, and rotate it if exposed.

Risk: Broad Zoho OAuth scopes or enabled write/delete tools can let an agent change or remove CRM records beyond the intended workflow.

Mitigation: Start with read-only scopes and enable create, update, or delete tools only for agents and tasks that explicitly require them.

Risk: Fixed temporary-file examples can leave request arguments on disk or collide across sessions.

Mitigation: Prefer the bundled Python helpers or secure, unique temporary files for shell-based JSON arguments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sprintcx/skills/zoho-crm-mcp)
- [Zoho CRM MCP portal](https://mcp.zoho.eu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and Python helper scripts that can print tables or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOHO_MCP_URL and mcporter; helper scripts may access CRM data according to the configured Zoho OAuth scopes.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
