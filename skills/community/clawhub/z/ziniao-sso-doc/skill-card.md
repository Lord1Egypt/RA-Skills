## Description:

Helps developers understand the Ziniao SSO OpenAPI capabilities, integration flow, and interface map for ERP single sign-on planning and evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziniao-open](https://clawhub.ai/user/ziniao-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ERP integration engineers use this skill to design Ziniao SSO integrations, identify required API calls, and route to detailed reference files for authentication, account lookup, user login, and client URL handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSO credentials such as API_Key, appAuthToken, and openapiToken may appear in headers, URLs, or command arguments.

Mitigation: Treat these values as secrets, avoid logging or sharing full Schema URLs, and prefer the documented no-token local-login path when available.

Risk: Debug ports, forced download paths, and no-prompt download behavior can change local browser and file-handling behavior.

Mitigation: Require explicit user or administrator approval before using those options.

Risk: Employee and account query responses can expose sensitive business data.

Mitigation: Limit access to authorized integration workflows and avoid copying returned employee or account details into shared logs or support bundles.

## Reference(s):

- [Ziniao SSO Skill Definition](artifact/SKILL.md)
- [Authentication and User Login Reference](artifact/reference/account-auth.md)
- [Company, Staff, and Account Query Reference](artifact/reference/account-crud.md)
- [API Usage Guide](artifact/reference/api-guide.md)
- [Client Schema URL Protocol Reference](artifact/reference/client-schema.md)
- [ClawHub Skill Release Page](https://clawhub.ai/ziniao-open/skills/ziniao-sso-doc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API paths, request examples, response handling notes, and integration flow summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no direct API calls are executed by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
