## Description:

Provision a YG3 marketing workspace and call 200+ MCP tools for content, SEO, sites, outbound, LinkedIn, and ads. No human signup required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slamdunkboy17](https://clawhub.ai/user/slamdunkboy17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous agents use this skill to provision YG3 marketing workspaces and operate live marketing workflows for sites, blogs, brand voice, SEO content, outbound, LinkedIn, and ads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The owner-claim flow asks an agent to handle a human password.

Mitigation: Do not provide reusable passwords to the agent; use OAuth, a browser-based claim flow, a one-time claim link, or another flow where the agent never sees the password.

Risk: Workspace tokens grant access to YG3 MCP operations.

Mitigation: Treat workspace tokens as secrets, avoid logging or publishing them, and reuse an existing token instead of provisioning duplicate workspaces.

Risk: The skill can publish live marketing content through YG3 services.

Mitigation: Review planned writes before confirmation and only publish public content when live YG3 marketing work is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slamdunkboy17/skills/yg3-marketing-mcp)
- [YG3 agent guide](https://www.yg3.ai/for-agents)
- [YG3 machine index](https://www.yg3.ai/llms.txt)
- [YG3 live tool catalog](https://mcp.yg3.ai/api/health)
- [YG3 MCP README](https://github.com/YG3-ai/yg3-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and MCP call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or use workspace tokens and live marketing API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
