## Description:

Provides local Feishu Open Platform API reference material with complete permissions, fields, examples, and documentation rules for Feishu-related work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as local reference material when documenting or working with Feishu Open Platform APIs for authentication, contacts, messaging, passport sessions, permissions, IDs, and request or response examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example code or placeholders may lead users to expose Feishu app secrets or access tokens if copied directly into projects.

Mitigation: Store credentials in secure storage or environment variables, replace placeholders deliberately, and avoid hardcoding secrets.

Risk: Contact or messaging API usage may access data outside the intended Feishu tenant scope if permissions are not checked.

Mitigation: Confirm the application has only the required Feishu tenant permissions and call APIs within the authorized scope.

Risk: Incomplete or simplified API documentation can cause incorrect Feishu requests or permission handling.

Mitigation: Use the included documentation rules and Feishu references to preserve complete parameters, permission notes, examples, and error-code guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lentiancn/skills/skill-feishu)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu API documentation](https://open.feishu.cn/document/server-docs)
- [Feishu app permission configuration](https://open.feishu.cn/document/ugTN1YjL4UTN24CO1UjN/uQzN1YjL0cTN24CN3UjN)
- [Feishu user identity introduction](https://open.feishu.cn/document/home/user-identity-introduction/introduction)
- [Feishu department ID field overview](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/field-overview)
- [Feishu scope authority guide](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/v3/guides/scope_authority)
- [Feishu common error codes](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN)
- [Local Feishu API index](open-apis/README.md)
- [Local Feishu API documentation template](open-apis/TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reference material with API examples, permission notes, configuration guidance, and documentation rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local reference content only; replace placeholders carefully and keep Feishu app credentials outside generated or copied code.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
