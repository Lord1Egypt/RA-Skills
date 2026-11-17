## Description:

Query and manage Salesforce CRM data via the Salesforce CLI (`sf`), including SOQL/SOSL queries, schema inspection, record operations, bulk import/export, Apex execution, metadata deployment, and raw REST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arvorco](https://clawhub.ai/user/arvorco)

### License/Terms of Use:


## Use Case:

Developers, Salesforce administrators, and CRM operations teams use this skill to ask an agent for Salesforce CLI commands and guidance for querying data, managing records, inspecting schemas, running Apex, deploying metadata, and making authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Salesforce CLI sessions can access or mutate sensitive CRM data.

Mitigation: Use least-privileged Salesforce users and sandbox orgs where possible, and require explicit confirmation before write, deploy, Apex, bulk, or raw REST operations.

Risk: Credential-revealing org display and auth URL commands can expose access tokens or refresh-token auth URLs.

Mitigation: Prefer browser login and do not print, save, or summarize access tokens, refresh-token auth URLs, or full org display JSON.

Risk: Bulk import, bulk delete, metadata deployment, Apex execution, and raw REST calls can create large or hard-to-reverse org changes.

Mitigation: Review files, queries, target org, and operation scope before execution; use small query limits for exploration.

## Reference(s):

- [Salesforce CLI Developer Tools](https://developer.salesforce.com/tools/salesforcecli)
- [Salesforce Skill on ClawHub](https://clawhub.ai/arvorco/skills/salesforce)
- [Salesforce CLI npm package](https://www.npmjs.com/package/@salesforce/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Salesforce CLI session; commands should prefer --json and prompt before write, deploy, Apex, bulk, or raw REST operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
