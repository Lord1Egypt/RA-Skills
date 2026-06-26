## Description: <br>
Complete Salesforce REST API for SOQL queries, CRUD operations, Bulk API, Composite API, authentication, and standard objects with error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to work with Salesforce REST APIs, including SOQL queries, record create/read/update/delete operations, bulk imports and exports, composite requests, metadata lookup, authentication setup, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, export, create, update, or delete Salesforce data using credentials supplied by the user. <br>
Mitigation: Use a sandbox or least-privilege Salesforce integration user when possible, and review write, delete, and bulk commands before execution. <br>
Risk: Salesforce access tokens and instance URLs are required for API calls. <br>
Mitigation: Keep secrets in environment variables, avoid pasting them into shared shells or logs, and rotate or revoke credentials according to Salesforce policy. <br>
Risk: Salesforce context and preferences may be retained locally under ~/salesforce-api-integration/. <br>
Mitigation: Inspect or remove the local directory when retained org context is no longer desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/salesforce-api-integration) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill Homepage](https://clawic.com/skills/salesforce-api-integration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, CSV, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Salesforce environment variables and may maintain local Salesforce preferences under ~/salesforce-api-integration/.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
