## Description: <br>
Full Salesflare API operations skill for reading, searching, creating, and updating CRM data across accounts, contacts, opportunities, tasks, pipelines, users, tags, workflows, and related Salesflare resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeroencorthout](https://clawhub.ai/user/jeroencorthout) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, operations, and developer users can use this skill to query Salesflare CRM records, inspect available API endpoints, build API-driven automations, and perform confirmed CRM updates or deletes through helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Salesflare CRM data when an agent has access to a Salesflare API key. <br>
Mitigation: Use a least-privileged API key, keep credentials in local environment storage, and confirm every write or delete with exact record IDs and payloads before execution. <br>
Risk: Smoke-test write modes can create, update, and delete temporary CRM records. <br>
Mitigation: Keep smoke tests in read-only mode by default and enable write or delete modes only in a workspace where temporary CRM test records are acceptable. <br>
Risk: Changing SALESFLARE_BASE_URL could send CRM requests to an unintended endpoint. <br>
Mitigation: Use the default Salesflare production API or a trusted staging endpoint, and review the configured base URL before running requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeroencorthout/salesflare) <br>
- [Salesflare API endpoint usage notes](references/endpoints.md) <br>
- [Salesflare API base URL](https://api.salesflare.com) <br>
- [Salesflare OpenAPI specification](https://api.salesflare.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown summaries with shell commands and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SALESFLARE_API_KEY and python3; default workflows read before writes and require explicit confirmation for mutations.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
