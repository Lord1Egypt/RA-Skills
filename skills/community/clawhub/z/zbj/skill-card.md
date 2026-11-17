## Description:

猪八戒网(ZBJ) MCP服务器 - AI智能需求发布、订单管理、服务搜索、类目匹配，连接百万服务商的一站式威客平台

This skill is ready for commercial/non-commercial use.

## Publisher:

[nylk](https://clawhub.ai/user/nylk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search ZBJ services and shops, match service categories, publish and manage demands, manage orders, evaluate sellers, and request payment links through ZBJ APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact ZBJ account and marketplace actions, including publishing or closing demands, selecting sellers, evaluating sellers, and generating payment links.

Mitigation: Use a dedicated least-privilege ZBJ_API_KEY and manually confirm every publish, close, winner-selection, evaluation, or payment-related action before execution.

Risk: ZBJ_API_URL is configurable, so the API key could be sent to a non-official endpoint if the environment is changed.

Mitigation: Keep ZBJ_API_URL set to https://zmcp.zbj.com unless operating a fully controlled endpoint, and review environment configuration before use.

## Reference(s):

- [ZBJ MCP homepage](https://zmcp.zbj.com)
- [ZBJ MCP documentation](https://zmcp.zbj.com/docs)
- [ClawHub skill page](https://clawhub.ai/nylk/skills/zbj)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON API responses with agent-facing text guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZBJ_API_KEY; keep ZBJ_API_URL on the official endpoint unless using a controlled deployment.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
