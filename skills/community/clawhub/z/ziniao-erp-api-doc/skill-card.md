## Description:

Provides documentation for planning and evaluating integrations with the Ziniao ERP REST API, including API capabilities, authentication, permissions, identifiers, response structure, and request flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziniao-open](https://clawhub.ai/user/ziniao-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to understand the Ziniao ERP API surface before designing ERP integrations or requesting required permission points. It is for API documentation lookup and planning, not for executing API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented ERP workflows involve sensitive values such as API keys, employee passwords, proxy credentials, mobile numbers, account IDs, and company data.

Mitigation: Treat those values as secrets and avoid pasting them into shared chats, logs, or generated examples.

Risk: The documented endpoints include high-impact administrative and billing actions such as deletions, authorization changes, role changes, cache clearing, device binding changes, purchases, renewals, and auto-renewal changes.

Mitigation: Require explicit user approval and verify target IDs, permission points, and business intent before using guidance for those operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziniao-open/skills/ziniao-erp-api-doc)
- [Publisher profile](https://clawhub.ai/user/ziniao-open)
- [Skill overview](artifact/SKILL.md)
- [API guide](artifact/reference/api-guide.md)
- [Account CRUD](artifact/reference/account-crud.md)
- [Account authorization](artifact/reference/account-auth.md)
- [Account tags](artifact/reference/account-tags.md)
- [Device management](artifact/reference/device-management.md)
- [Access policy web management](artifact/reference/access-policy-web.md)
- [Access policy rules](artifact/reference/access-policy-rules.md)
- [Roles and permissions](artifact/reference/roles-permissions.md)
- [Department and staff](artifact/reference/department-staff.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration guidance]

**Output Format:** [Markdown guidance with API paths, request fields, response notes, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; does not install code, run commands, persist state, or call APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
