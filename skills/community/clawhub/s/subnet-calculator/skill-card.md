## Description:

一个基于Model Context Protocol的服务，提供IPv4子网规划工具，包括子网大小计算、通配符掩码生成、网关选择和主机验证等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers, developers, and operators use this skill to calculate IPv4 subnet plans, OSPF wildcard masks, gateway context, host membership, and usable host addresses through a XiaoBenYang-backed service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and stores it in a plaintext .env file.

Mitigation: Use a limited or revocable key, avoid shared or committed workspaces, and delete or protect the .env file after use.

Risk: Subnet inputs are sent to an external XiaoBenYang service.

Mitigation: Use the skill only with subnet data that may be shared with that service.

Risk: The artifact contains unrelated gaokao naming remnants.

Mitigation: Ask the publisher to clarify the naming mismatch before routine or sensitive use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alinklab/skills/subnet-calculator)
- [ALinkLab Publisher Profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API Key Site](https://xiaobenyang.com)
- [XiaoBenYang MCP Service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration Guidance]

**Output Format:** [Markdown or concise text summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; tool calls return success, message, and raw JSON fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
