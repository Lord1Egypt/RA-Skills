## Description:

股票多条件筛选、热门因子管理、Jiuyan 数据查询和抖音热点分析。提供 17 个 CLI 工具覆盖四大模块。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query and compare stock data, manage hot-factor presets, retrieve Jiuyan stock analysis, and inspect Douyin hotspot data through CLI tools backed by a configured API server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an API key to a configurable API server.

Mitigation: Install only with a trusted API server, prefer HTTPS for remote endpoints, and use a narrowly scoped, revocable STOCK_API_KEY.

Risk: Hot-factor create, update, sort, and delete tools can mutate or delete remote presets.

Mitigation: Require confirmation before running preset-changing tools and avoid allowing untrusted prompts or pasted identifiers to trigger those actions.

Risk: Stock analysis, comparison, and hotspot outputs depend on the configured backend API.

Mitigation: Treat returned data as backend-provided analysis and verify important investment or operational decisions with authoritative sources.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/afengzi/skills/stock-filter-skills)
- [Publisher profile](https://clawhub.ai/user/afengzi)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON-formatted text from CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, STOCK_API_BASE_URL, and STOCK_API_KEY for authenticated API requests.]

## Skill Version(s):

1.3.0 (source: evidence.json release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
