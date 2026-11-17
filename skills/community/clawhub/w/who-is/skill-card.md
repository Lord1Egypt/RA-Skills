## Description:

一个基于Model Context Protocol (MCP)的WHOIS域名查询服务器，支持877+顶级域名和169个国家代码顶级域名的解析，提供全面的域名注册信息查询功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up domain registration details, refresh WHOIS server mappings, and list supported top-level domains through the provided tool functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain queries and API calls are proxied through the external XiaoBenYang service.

Mitigation: Use only after deciding that the upstream service is trusted for the domains being queried and the associated API usage.

Risk: The API key is persisted as plaintext in the workspace .env file.

Mitigation: Avoid shared or source-controlled workspaces, protect the .env file, and rotate the key if it may have been exposed.

Risk: The artifact contains mismatched gaokao/education configuration remnants.

Mitigation: Review and clean stale configuration or documentation before deployment so operators understand the actual WHOIS data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/who-is)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key page](https://xiaobenyang.com)
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries of JSON-derived WHOIS results and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY; raw WHOIS response data may be included when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
