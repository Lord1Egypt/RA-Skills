## Description: <br>
Provides a local Markdown reference for Feishu Open Platform APIs, including permissions, fields, request and response examples, and documentation rules that require complete, verifiable API records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as local Feishu API reference material when creating, reviewing, or updating Feishu integrations that involve authentication, contacts, messaging, and session APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu API examples involve credentials, OAuth tokens, directory data, sessions, and messaging operations that may expose sensitive information if copied into production without controls. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid logging raw token or directory responses, and treat contact, session, and messaging APIs as sensitive administrative operations. <br>
Risk: Over-broad Feishu scopes can grant access to more contact or user data than an integration needs. <br>
Mitigation: Request the minimum Feishu scopes needed for the target operation and review each documented permission before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lentiancn/skill-feishu) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Feishu API documentation](https://open.feishu.cn/document/server-docs) <br>
- [Feishu app permission configuration](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN) <br>
- [Feishu user identity concepts](https://open.feishu.cn/document/home/user-identity-introduction/introduction) <br>
- [Feishu department ID overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview) <br>
- [Feishu permission scope guidance](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority) <br>
- [Feishu common error codes](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown documentation with API tables and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference material; examples may include placeholder Feishu tokens, scopes, API paths, request bodies, and response bodies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
