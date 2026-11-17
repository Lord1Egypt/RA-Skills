## Description:

Use b24 to read and change a Bitrix24 portal's CRM - deals, leads, pipelines and the funnel, contacts (people), companies (organizations), products, employees - with the owner's profile and JSON answers; deals and leads are synced into the local WireCat store. Use when a question could be answered from the owner's Bitrix24 sales data (how a deal stands, what is open, who a client is), when the owner asks to create, move, close or change a CRM record, or to set b24 up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to answer questions from an owner's Bitrix24 CRM and, when explicitly requested, make specific CRM changes. It also guides setup of the b24 command line tool and its optional MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags that destructive CRM actions may lack confirmation.

Mitigation: Only make the exact change the owner requested, inspect --dry-run permission details first, and configure MCP write permissions as readonly or deny (or enable client-side approval) for actions that must wait for approval.

Risk: Search can include messages and notes beyond the stated purpose, which may expose more CRM content than needed.

Mitigation: Use the narrowest search and record fields needed for the task, and consider the message and note scope before enabling or running broad searches.

Risk: The security analysis is partial because two local references could not be resolved.

Mitigation: Review the unresolved references and complete the security review before relying on the scan as a complete assessment.

## Reference(s):

- [Reading the CRM](references/reading.md)
- [Writing to the CRM](references/writing.md)
- [b24 over MCP](references/mcp.md)
- [Output and exit codes](references/output.md)
- [Setting b24 up](references/setup.md)
- [MCP guide](https://github.com/WireCatLabs/bitrix24-cli/blob/main/docs/mcp.md)
- [Permissions guide](https://github.com/WireCatLabs/bitrix24-cli/blob/main/docs/permissions.md)
- [Usage guide](https://github.com/WireCatLabs/bitrix24-cli/blob/main/docs/usage.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON CRM results with concise text or Markdown summaries; shell commands and configuration guidance for setup or requested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain sensitive CRM information; include only the client details needed for the owner's request.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
