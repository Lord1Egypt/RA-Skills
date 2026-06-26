## Description: <br>
Salesforce CRM integration with managed OAuth. Manage accounts, contacts, leads, opportunities, campaigns, tasks, reports, SOQL queries, and SObject records through the Salesforce REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, sales operations teams, and developers use this skill to inspect and manage Salesforce CRM data through ClawLink-managed OAuth. It supports read, query, create, update, delete, bulk, file, report, and Salesforce metadata workflows when the connected account has the needed permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: With sufficient Salesforce permissions, the skill can change or delete live Salesforce records, files, and schema. <br>
Mitigation: Use a Salesforce account with only the permissions needed for the task, and require a clear preview plus explicit approval before write, delete, bulk, file, or schema actions. <br>
Risk: Salesforce access is mediated through ClawLink OAuth and depends on the connected account and granted scopes. <br>
Mitigation: Install only if you trust ClawLink to broker the connection, verify the active Salesforce integration, and reconnect through the ClawLink dashboard if tools are missing or stale. <br>


## Reference(s): <br>
- [ClawHub Salesforce Skill Page](https://clawhub.ai/hith3sh/salesforce-ops) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [Salesforce REST API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_rest.api.meta/api_rest/) <br>
- [Salesforce SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_samples_soql.htm) <br>
- [Salesforce SOSL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_samples_sosl.htm) <br>
- [Salesforce SObject Reference](https://developer.salesforce.com/docs/atlas.en-us.api_rest.api.meta/api_rest/resources_sobjects.htm) <br>
- [Salesforce Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.api.meta/api_asynch/bulk_api_2_0.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Salesforce account through ClawLink OAuth; write operations should be previewed and explicitly approved.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
