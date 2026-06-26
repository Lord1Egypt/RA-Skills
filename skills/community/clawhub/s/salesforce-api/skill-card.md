## Description: <br>
Salesforce CRM API integration with managed OAuth for querying records with SOQL, managing sObjects, and performing CRM CRUD operations through Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and CRM administrators use this skill to access Salesforce CRM data through Maton, including querying records, managing OAuth connections, and performing specific create, update, delete, batch, and composite actions after user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Salesforce CRM data through Maton. <br>
Mitigation: Use the narrowest Salesforce permissions available, prefer sandbox orgs for destructive or batch work, and require explicit approval before writes or deletes. <br>
Risk: Requests may run against the wrong Salesforce connection when multiple connections exist. <br>
Mitigation: Verify and explicitly specify the intended connection ID before each request. <br>
Risk: MATON_API_KEY is a sensitive credential. <br>
Mitigation: Do not expose the key in chats, logs, shared files, or outputs, and revoke or rotate unused or exposed credentials promptly. <br>


## Reference(s): <br>
- [ClawHub Salesforce skill page](https://clawhub.ai/byungkyu/salesforce-api) <br>
- [Salesforce REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm) <br>
- [Salesforce SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm) <br>
- [Salesforce Composite Request](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_composite_composite_post.htm) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and a Salesforce OAuth connection scoped to the requested resources.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
