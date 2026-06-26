## Description: <br>
Read-only CLI access to ServiceNow Table, Attachment, Aggregate, and Service Catalog APIs; includes schema inspection and history retrieval (read-only). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and support agents use this skill to read ServiceNow records, attachments, aggregate statistics, schemas, ticket history, and service catalog data through a read-only Node.js CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ServiceNow credentials may be exposed if passed directly on the command line or stored insecurely. <br>
Mitigation: Use a scoped read-only ServiceNow account and prefer environment variables or a protected .env file over command-line passwords. <br>
Risk: Read access can expose sensitive ServiceNow records, ticket history, or attachment content. <br>
Mitigation: Keep queries narrow with sysparm_limit and sysparm_fields, and download only the specific attachments needed for the task. <br>
Risk: The bundled reference YAML files include non-GET endpoints even though the skill is intended to be read-only. <br>
Mitigation: Use only documented GET operations and ignore any POST, PUT, PATCH, or DELETE endpoints present in the reference files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheSethRose/servicenow-agent) <br>
- [Table API reference](references/table-api.yaml) <br>
- [Attachment API reference](references/attachment.yaml) <br>
- [Aggregate API reference](references/aggregate-api.yaml) <br>
- [Service Catalog API reference](references/service-catalog-api.yaml) <br>
- [ServiceNow Table API documentation](https://docs.servicenow.com/?context=CSHelp:REST-Table-API) <br>
- [ServiceNow Attachment API documentation](https://docs.servicenow.com/?context=CSHelp:REST-Attachment-API) <br>
- [ServiceNow Aggregate API documentation](https://docs.servicenow.com/?context=CSHelp:REST-Aggregate-API) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON API responses, and optional binary attachment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Attachment content can be saved to a local file with --out; normal Table API results are returned under result.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
