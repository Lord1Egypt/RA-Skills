## Description:

Read-only CLI access to ServiceNow Table, Attachment, Aggregate, and Service Catalog APIs; includes schema inspection and history retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers, support engineers, and service desk operators use this skill to inspect ServiceNow records, incidents, attachments, aggregate statistics, schemas, history, and service catalog data from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and ServiceNow access could expose account secrets or sensitive ticket data.

Mitigation: Use a dedicated, least-privilege, read-only ServiceNow account; use HTTPS-only domains; avoid command-line passwords; and keep .env out of shared folders and version control.

Risk: Ticket history, work notes, and attachments may contain sensitive business or personal information.

Mitigation: Limit queries with sysparm_limit and sysparm_fields, review outputs before sharing, and treat downloaded attachment content as sensitive.

Risk: The skill is documented as read-only, but included API reference files contain mutating ServiceNow operations.

Mitigation: Do not rely on the reference files alone as a safe read-only surface; remove or technically block mutating operations before installation.

## Reference(s):

- [ServiceNow Table API reference](references/table-api.yaml)
- [ServiceNow Attachment API reference](references/attachment.yaml)
- [ServiceNow Aggregate API reference](references/aggregate-api.yaml)
- [ServiceNow Service Catalog API reference](references/service-catalog-api.yaml)
- [ServiceNow REST Table API documentation](https://docs.servicenow.com/?context=CSHelp:REST-Table-API)
- [ServiceNow REST Attachment API documentation](https://docs.servicenow.com/?context=CSHelp:REST-Attachment-API)
- [ServiceNow REST Aggregate API documentation](https://docs.servicenow.com/?context=CSHelp:REST-Aggregate-API)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save binary attachment content to a user-specified output path.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
