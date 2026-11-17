## Description:

Manage Salesforce CRM records through the Salesforce CLI and REST API, including querying, creating, updating, deleting, and reporting on contacts, accounts, opportunities, leads, cases, and tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-riverbi](https://clawhub.ai/user/lucas-riverbi)

### License/Terms of Use:

MIT

## Use Case:

Sales, support, and operations teams use this skill through an agent to inspect and manage Salesforce CRM data, run SOQL queries, create records, update pipeline or activity data, and perform bulk import or export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, create, update, delete, bulk import, and bulk export live Salesforce CRM data.

Mitigation: Install only for agents and users authorized to operate on the selected Salesforce org, prefer a sandbox first, and require explicit human confirmation before create, update, delete, bulk, arbitrary SOQL, or schema-discovery operations.

Risk: Salesforce credentials or access tokens could be exposed if pasted into chat, command history, or logs.

Mitigation: Use the Salesforce CLI authentication flows where possible, avoid pasting raw access tokens into chat or logs, and use a least-privilege Salesforce integration user.

Risk: Arbitrary SOQL and schema-discovery commands can expose sensitive CRM records or metadata.

Mitigation: Limit access to trusted users, apply least-privilege Salesforce permissions, and review queries before execution.

## Reference(s):

- [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli)
- [ClawHub Skill Page](https://clawhub.ai/lucas-riverbi/skills/salesforce-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Salesforce CLI, SOQL, REST API, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that read, create, update, delete, import, export, or describe Salesforce CRM data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
