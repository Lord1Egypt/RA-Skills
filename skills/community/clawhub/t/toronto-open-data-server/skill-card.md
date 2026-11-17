## Description:

一个通过CKAN API直接访问多伦多开放数据的MCP服务器，支持智能数据集发现、灵活查询和CSV数据预览，专为LLM代理设计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to discover Toronto Open Data datasets, inspect dataset schemas and statistics, query available records, and preview CSV-backed resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Toronto data queries, filters, natural-language questions, CSV URLs, and the Xiaobenyang API key are sent to a third-party intermediary.

Mitigation: Use the skill only when that intermediary is trusted, avoid sensitive query content, and review whether a direct Toronto Open Data integration is preferable.

Risk: The API key is persisted in a local .env file, which can be exposed in shared workspaces or repositories.

Mitigation: Keep credentials out of shared repositories, prefer session-only secrets where possible, and rotate the key if it may have been exposed.

Risk: The public description presents the skill as direct CKAN access even though server evidence identifies a third-party proxy.

Mitigation: Disclose the Xiaobenyang dependency to users before installation and verify that transmitted data is acceptable for the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/toronto-open-data-server)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and may return dataset listings, schemas, query results, statistics, CSV previews, or follow-up guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
