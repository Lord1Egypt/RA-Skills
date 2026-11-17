## Description:

Query Salesforce data and manage sales pipelines using the `sf` CLI for SOQL queries, opportunity analysis, forecast reporting, data exports, schema exploration, and CRM data operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rjmcgirr-pl](https://clawhub.ai/user/rjmcgirr-pl)

### License/Terms of Use:


## Use Case:

Employees, developers, and sales operations teams use this skill to query Salesforce, inspect schema, analyze opportunity pipeline and forecasts, export CRM data, and prepare sales workflows through the sf CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Salesforce CLI commands can read or export sensitive CRM data.

Mitigation: Use least-privilege Salesforce access, limit selected fields and result sizes, and review export commands before execution.

Risk: The skill includes commands for creating, updating, and bulk upserting Salesforce records.

Mitigation: Review write commands before running them, prefer sandbox testing, and restrict production permissions to necessary objects and fields.

Risk: The schema export script writes an object-specific markdown file in the current directory.

Mitigation: Use trusted object names and run the script only in directories where overwriting an existing schema file would be acceptable.

## Reference(s):

- [Pipeline & Forecast Queries](references/pipeline-queries.md)
- [Advanced SOQL Patterns](references/soql-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and SOQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Salesforce CLI commands that read, export, create, update, or upsert CRM records.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
