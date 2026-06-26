## Description: <br>
Manage Salesforce CRM records through Salesforce CLI and REST API workflows for querying, creating, updating, deleting, reporting on, and exporting CRM data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-riverbi](https://clawhub.ai/user/lucas-riverbi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and CRM administrators use this skill to guide Salesforce CLI and REST API operations for contacts, accounts, opportunities, leads, cases, tasks, pipeline reports, and bulk CSV workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, bulk import, bulk export, or perform REST API actions against live Salesforce CRM data. <br>
Mitigation: Use a least-privilege Salesforce account, set and verify SALESFORCE_TARGET_ORG, test in a sandbox first, and require explicit confirmation before write, delete, bulk, export, or REST API actions. <br>
Risk: Queries and exports can expose sensitive CRM records such as contacts, accounts, opportunities, leads, cases, and tasks. <br>
Mitigation: Limit access to authorized users and orgs, prefer scoped queries, avoid unnecessary exports, and handle CSV or JSON outputs according to the organization's data policy. <br>


## Reference(s): <br>
- [Salesforce CLI Documentation](https://developer.salesforce.com/tools/salesforcecli) <br>
- [ClawHub Salesforce Skill Release](https://clawhub.ai/lucas-riverbi/salesforce-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, SOQL, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Salesforce CLI commands and REST API examples that operate on the configured target org.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
