## Description:

Deploy and manage serverless applications on Volcengine veFaaS through the `vefaas` CLI. Use when the user has chosen veFaaS or is working with existing veFaaS resources: deploy web apps, static sites, or MCP servers to veFaaS, manage applications and functions (pull/push code, release, rollback, invoke, logs), configure environment variables, manage sandboxes and gateways, inspect veFaaS projects, troubleshoot vefaas CLI/auth/framework/gateway issues, call veFaaS OpenAPI, or look up veFaaS docs and SDK usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers working with Volcengine veFaaS use this skill to deploy and manage applications, functions, sandboxes, MCP servers, and OpenAPI integrations through the vefaas CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud actions can expose endpoints, change resources, or incur costs.

Mitigation: Use credentials scoped to the intended resources and confirm the account, resource IDs, public endpoints, and expected costs before deployment or deletion.

## Reference(s):

- [Application workflow](references/vefaas-application.md)
- [Authentication and credentials](references/vefaas-auth.md)
- [CLI and versions](references/vefaas-cli.md)
- [Official documentation workflow](references/vefaas-docs.md)
- [Function management](references/vefaas-function.md)
- [OpenAPI calls](references/vefaas-openapi.md)
- [Sandbox management](references/vefaas-sandbox.md)
- [Triggers and APIG routes](references/vefaas-trigger.md)
- [MCP deployment](references/mcp-deployment.md)
- [Troubleshooting](references/vefaas-troubleshooting.md)
- [ClawHub release page](https://clawhub.ai/volc-sdk-team/skills/volcengine-vefaas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with command examples and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
