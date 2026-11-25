## Description:

Use b24 to read and change a Bitrix24 portal's CRM - deals, leads, pipelines and the funnel, contacts (people), companies (organizations), products, employees, and client files such as contracts, invoices and attachments - with the owner's profile and JSON answers; deals and leads are synced into the local WireCat store. Use when a question could be answered from the owner's Bitrix24 sales data (how a deal stands, what is open, who a client is), when the owner asks to create, move, close or change a CRM record, or to set b24 up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to query a Bitrix24 portal's CRM and, when explicitly requested, create or change specific CRM records. It also guides users through setup and safe use of the b24 command line and MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: With MCP enabled, writes may proceed without an interactive confirmation even when a permission is set to ask; a CRM change can trigger portal workflows that contact or bill clients.

Mitigation: Review MCP write behavior before installation. Set permissions to readonly or deny for writes that must not proceed without owner approval, or enable approval for b24_write in the MCP client.

Risk: Search can access messages and notes beyond the declared CRM scope.

Mitigation: Consider whether access to messages and notes is appropriate for the intended use before installation and use.

## Reference(s):

- [Bitrix24 Cli on ClawHub](https://clawhub.ai/wirecat/skills/wirecat-b24)
- [Reading the CRM](references/reading.md)
- [Writing the CRM](references/writing.md)
- [b24 over MCP](references/mcp.md)
- [Setting b24 up](references/setup.md)
- [Output and exit codes](references/output.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command results with concise natural-language answers and Markdown shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers reflect the selected profile, stored data scope, sync freshness, and portal permissions.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
