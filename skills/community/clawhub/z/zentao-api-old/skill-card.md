## Description:

Integrates an agent with ZenTao Legacy API 1.0 to manage projects, products, tasks, bugs, requirements, tests, versions, releases, and related workflow records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellotombruce](https://clawhub.ai/user/hellotombruce)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, product managers, and QA teams use this skill to let an agent query and update ZenTao work items, including projects, tasks, bugs, requirements, test cases, plans, and releases. It is intended for ZenTao instances that still use Legacy API 1.0 workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads ZenTao endpoint, username, and password values and persists session material locally.

Mitigation: Use a least-privilege ZenTao account, require HTTPS, avoid printing credentials, restrict file permissions, and keep TOOLS.md and .zentao/ out of source control.

Risk: The skill can perform live write actions such as creating, assigning, closing, canceling, and deleting project-management records.

Mitigation: Test against a non-production ZenTao instance first and require manual confirmation before delete, close, cancel, restore, admin, or bulk operations.

Risk: The security verdict is suspicious due to credential/session handling and live system mutation capabilities.

Mitigation: Review the package and security guidance before installation, and deploy only where the connected ZenTao permissions match the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellotombruce/skills/zentao-api-old)
- [ZenTao official website](https://www.zentao.net/)
- [ZenTao API documentation](https://www.zentao.net/book/zentaopmshelp/562.html)
- [ZenTao API v1 documentation](https://zentao.net/book/apidoc-v1/apidoc-v1.html)
- [Artifact README](README.md)
- [Artifact API index](docs/index.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls, Markdown]

**Output Format:** [Markdown guidance with Python examples, shell commands, and ZenTao API call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify records in a live ZenTao system when used with valid credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
