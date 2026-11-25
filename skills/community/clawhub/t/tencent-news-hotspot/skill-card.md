## Description:

当用户要求按领域或频道汇总腾讯新闻热点精选内容时使用，例如「聚合近期财经股票热点新闻」「帮我汇总下今天的体育热点新闻」「整理下本周科技领域的重要新闻」。通过腾讯新闻 CLI 的 hotspot 命令按频道 pool_tag_id 拉取精选文章并整理输出；频道不支持、时间范围无法覆盖或无数据时如实说明。不用于实时比分、天气、早晚报、股票行情或事实核查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request a digest of Tencent News featured articles for a supported channel or topic, covering today, this week, or a recent period. The skill returns article details and summaries, and reports unavailable channels, missing data, or query failures clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious because its news-summary purpose is paired with unverified remote installer or update commands and a reported action that clears the CLI API key. The scan was partial: 14 of 16 components were fully inspected, with limited analysis of two shell scripts.

Mitigation: Before installation, seek assurance that installer and update scripts are authenticated, software changes require approval, and API-key clearing is removed or explicitly justified. Treat the remaining script behavior as not fully assessed.

## Reference(s):

- [Channel mapping and time-range guidance](references/hotspot-channels.md)
- [CLI integration and query format](references/cli-integration.md)
- [CLI environment and failure handling](references/cli-environment.md)
- [Tencent News premium-list API documentation](https://openapi.inews.woa.com/docs/premium_list)
- [Skill release page](https://clawhub.ai/tencent-adm/skills/tencent-news-hotspot)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown article digest with titles, publication times, sources, links, and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Channel and time range vary by request; reports missing fields and partial results when data is unavailable.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
