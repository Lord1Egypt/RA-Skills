## Description:

Query Topical topic intelligence via MCP - breaking news, signals, trends, and source links from scheduled runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveangelcode](https://clawhub.ai/user/daveangelcode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve scheduled Topical intelligence, prepare topic briefings or monitoring updates, and configure Topical MCP and OpenClaw webhook delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook path can automatically wake and direct an agent with externally supplied content.

Mitigation: Review before installing, use a least-privileged OpenClaw agent for Topical webhooks, and consider setting deliver=false until the flow is trusted.

Risk: Webhook authorization and signature handling may be insufficient if the gateway does not enforce them.

Mitigation: Keep the hook bearer token strong and do not rely on the transform alone for Topical signature verification unless gateway-level verification is separately enforced.

## Reference(s):

- [Topical homepage](https://usetopical.com)
- [Topical OpenClaw portal](https://app.usetopical.com/portal/openclaw/)
- [ClawHub Topical skill](https://clawhub.ai/daveangelcode/skills/topical)
- [ClawHub Topical OpenClaw setup skill](https://clawhub.ai/daveangelcode/skills/topical-openclaw-setup)
- [Topical agent webhook payloads](references/payloads.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference MCP tool calls, OpenClaw configuration, webhook transform files, and source URLs from Topical results.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
