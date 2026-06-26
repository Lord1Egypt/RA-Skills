## Description: <br>
Guides ERP and integration engineers through Ziniao SSO OpenAPI capabilities, integration flow, authentication modes, interface routing, and Windows client Schema URL usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziniao-open](https://clawhub.ai/user/ziniao-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to plan and evaluate ERP single sign-on integrations with Ziniao, including API authentication, company, employee, account, and user login token flows. It also helps agents route detailed parameter lookup to the appropriate reference document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses API keys, app tokens, user login tokens, employee lists, account mappings, and superbrowser:// links that may expose or control business account access. <br>
Mitigation: Treat these values as sensitive, use only authorized business access, minimize queries, and avoid pasting secrets or account data into chats or logs. <br>
Risk: Schema URL actions can open accounts, close accounts, or exit the Ziniao browser on supported Windows clients. <br>
Mitigation: Confirm the intended user, account, client environment, and action with the user before calling APIs or opening, closing, or exiting browser sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziniao-open/ziniao-sso-doc) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Authentication interfaces](artifact/reference/account-auth.md) <br>
- [Company, staff, and account query interfaces](artifact/reference/account-crud.md) <br>
- [API usage guide](artifact/reference/api-guide.md) <br>
- [Client Schema URL protocol](artifact/reference/client-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, JSON examples, curl commands, and Schema URL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; does not install code or perform actions itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
