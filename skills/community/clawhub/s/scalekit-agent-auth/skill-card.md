## Description:

Scalekit Agent Auth helps OpenClaw agents discover, authorize, and execute tools across connected third-party services through Scalekit Connect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avinash-kamath](https://clawhub.ai/user/avinash-kamath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let OpenClaw agents connect to SaaS services, verify authorization, inspect tool schemas, execute available tools, and fall back to proxied API calls when no catalog tool is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose raw OAuth access and refresh tokens through the authorization inspection command.

Mitigation: Do not use --get-authorization in agent workflows, and prefer a release that removes raw token printing.

Risk: Proxied API calls and upload/download flows can perform high-impact actions against connected services.

Mitigation: Review proxy upload, download, write, and broad-scope requests before execution and grant only the minimum OAuth scopes needed.

Risk: The skill depends on a trusted Scalekit environment and operator-controlled credentials.

Mitigation: Install only in trusted environments and protect TOOL_CLIENT_ID, TOOL_CLIENT_SECRET, TOOL_ENV_URL, and TOOL_IDENTIFIER as sensitive configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/avinash-kamath/skills/scalekit-agent-auth)
- [OpenClaw](https://openclaw.ai)
- [Scalekit Connect](https://scalekit.com)
- [Scalekit Dashboard](https://app.scalekit.com)
- [Scalekit Notion Connector Setup Guide](https://docs.scalekit.com/reference/agent-connectors/notion/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger connected-service API calls and proxied upload/download workflows through configured Scalekit connections.]

## Skill Version(s):

2.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
