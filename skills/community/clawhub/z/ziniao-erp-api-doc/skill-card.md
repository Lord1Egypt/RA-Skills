## Description: <br>
Helps agents understand the positioning, capabilities, permission model, and call flow of the Ziniao ERP API for ERP integration planning, system design, and interface evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziniao-open](https://clawhub.ai/user/ziniao-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ERP integration teams use this skill to plan integrations with the Ziniao ERP REST API, understand required permissions, and choose the correct reference file for detailed endpoint parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced ERP operations can affect accounts, authorizations, caches, roles, staff, access policies, and device purchases or renewals. <br>
Mitigation: Require explicit human review before using the guidance for destructive, permission-changing, or billable operations. <br>
Risk: Implementations based on the documentation may handle API keys, passwords, or other sensitive ERP credentials. <br>
Mitigation: Protect secrets, avoid exposing credentials in prompts or logs, and request only the ERP permissions needed for the integration. <br>


## Reference(s): <br>
- [Ziniao ERP API overview](artifact/SKILL.md) <br>
- [API guide](artifact/reference/api-guide.md) <br>
- [Account CRUD reference](artifact/reference/account-crud.md) <br>
- [Account authorization reference](artifact/reference/account-auth.md) <br>
- [Account tags reference](artifact/reference/account-tags.md) <br>
- [Device management reference](artifact/reference/device-management.md) <br>
- [Access policy web reference](artifact/reference/access-policy-web.md) <br>
- [Access policy rules reference](artifact/reference/access-policy-rules.md) <br>
- [Roles and permissions reference](artifact/reference/roles-permissions.md) <br>
- [Department and staff reference](artifact/reference/department-staff.md) <br>
- [ClawHub skill page](https://clawhub.ai/ziniao-open/ziniao-erp-api-doc) <br>
- [Publisher profile](https://clawhub.ai/user/ziniao-open) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with endpoint paths, JSON request and response shapes, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; does not run commands or make API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
