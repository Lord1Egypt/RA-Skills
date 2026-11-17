## Description:

Connect your AI agent to ServiceNow to query, create, update, and manage records across any table using the Table API and Stats API, including CRUD operations, aggregate analytics, schema introspection, and attachment management for ITSM, ITOM, and CMDB workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyflowstech](https://clawhub.ai/user/onlyflowstech)

### License/Terms of Use:

MIT

## Use Case:

Developers, administrators, and operations teams use this skill to let an agent inspect and manage ServiceNow records, attachments, aggregate reports, schemas, and instance health from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, delete, and batch-change ServiceNow records across tables.

Mitigation: Require human review for create, update, delete, batch, and attachment actions, and use the built-in confirm and dry-run controls for destructive or bulk operations.

Risk: The skill uses reusable ServiceNow credentials supplied through environment variables.

Mitigation: Use a dedicated least-privilege ServiceNow integration account, avoid admin credentials, and manage secrets through the host environment rather than committing them to files.

Risk: Misconfigured instance URLs or credential handling could expose operational data.

Mitigation: Set SN_INSTANCE to an HTTPS ServiceNow URL and review HTTPS validation and credential-handling behavior before production deployment.

## Reference(s):

- [ClawHub ServiceNow skill page](https://clawhub.ai/onlyflowstech/skills/servicenow)
- [OnlyFlows](https://onlyflows.tech)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq plus SN_INSTANCE, SN_USER, and SN_PASSWORD environment variables.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
