## Description:

查询搜索和获取博物馆的开放藏品数据

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and collection researchers use this skill to list Met Museum departments, search collection object IDs, and retrieve details for specific museum objects through a XiaoBenYang-backed MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and stores it in plaintext in the workspace .env file.

Mitigation: Use a dedicated low-value or revocable key, avoid reusable credentials, and review or change credential storage before production use.

Risk: Museum queries are routed through a configurable third-party MCP service that the security evidence flags as not clearly aligned with the advertised Met Museum purpose.

Mitigation: Confirm the endpoint, MCP identifier, tool behavior, and data flow before using the skill with sensitive requests or valuable credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/the-met)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and external MCP service access.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
