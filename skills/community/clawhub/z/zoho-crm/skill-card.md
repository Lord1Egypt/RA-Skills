## Description: <br>
Zoho CRM API integration with managed OAuth for reading, creating, updating, deleting, searching, and managing CRM records, organization settings, users, and module metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Zoho CRM through Maton's managed OAuth proxy, including CRM record CRUD, search, sales pipeline access, organization details, user management, and metadata retrieval. It is intended for workflows where the user has a valid Maton API key and an authorized Zoho CRM connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Zoho CRM data through Maton using a sensitive API key. <br>
Mitigation: Install only when Maton is trusted for the intended account, store MATON_API_KEY securely, and avoid exposing it in logs, command history, or shared terminals. <br>
Risk: Create, update, delete, bulk, user, and account-management operations can change CRM records or account state. <br>
Mitigation: Require explicit user approval before write or administrative operations, confirming the target resource, selected connection, and intended effect. <br>
Risk: When multiple Zoho CRM connections exist, requests could target the wrong account. <br>
Mitigation: Use the Maton-Connection header to select the intended connection before reading or changing CRM data. <br>


## Reference(s): <br>
- [ClawHub Zoho CRM Skill Page](https://clawhub.ai/byungkyu/zoho-crm) <br>
- [Related ClawHub API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Maton](https://maton.ai) <br>
- [Maton Settings](https://maton.ai/settings) <br>
- [Zoho CRM API v8 Documentation](https://www.zoho.com/crm/developer/docs/api/v8/) <br>
- [Zoho CRM Get Records API](https://www.zoho.com/crm/developer/docs/api/v8/get-records.html) <br>
- [Zoho CRM Insert Records API](https://www.zoho.com/crm/developer/docs/api/v8/insert-records.html) <br>
- [Zoho CRM Update Records API](https://www.zoho.com/crm/developer/docs/api/v8/update-records.html) <br>
- [Zoho CRM Delete Records API](https://www.zoho.com/crm/developer/docs/api/v8/delete-records.html) <br>
- [Zoho CRM Search Records API](https://www.zoho.com/crm/developer/docs/api/v8/search-records.html) <br>
- [Zoho CRM Users API](https://www.zoho.com/crm/developer/docs/api/v8/get-users.html) <br>
- [Zoho CRM Modules API](https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell, Python, JavaScript, HTTP examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Zoho CRM OAuth connection.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
