## Description:

联网搜索统一接口 - 自动选择最优服务商，支持降级、合并、告警

This skill is ready for commercial/non-commercial use.

## Publisher:

[naive-white-expert](https://clawhub.ai/user/naive-white-expert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web searches through one interface that selects configured providers, applies routing and filters, and returns answers, sources, provider details, and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, filters, and related metadata may be sent to the configured external search providers.

Mitigation: Configure only approved providers and avoid searching for secrets, regulated data, or other sensitive information.

Risk: The dependency guidance includes an unpinned requests install instruction.

Mitigation: Install in a controlled environment and pin or audit dependencies according to local policy until the publisher updates dependency guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naive-white-expert/skills/unified-web-search)
- [Publisher profile](https://clawhub.ai/user/naive-white-expert)
- [Project homepage](https://github.com/naive-white-expert/unified-web-search)
- [Service provider comparison](references/comparison.md)
- [Volcengine key types](references/volcengine-key-types.md)
- [DashScope](https://dashscope.aliyun.com/)
- [Tavily](https://tavily.com/)
- [Volcengine Search API endpoint](https://open.feedcoopapi.com/search_api/web_search)
- [Volcengine Search console](https://console.volcengine.com/search-infinity/api-key)
- [Volcengine Ark console](https://console.volcengine.com/ark/)
- [Volcengine Agent Plan console](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with answer text, sources, provider names, alerts, and applied filter metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one configured external search provider API key.]

## Skill Version(s):

2.2.1 (source: server release metadata; SKILL.md frontmatter states 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
