## Description:

微博/小红书/抖音/知乎/百度热搜与舆情分析助手。一句话查热搜榜、对话题做声量/情感/互动/平台分布分析、采样原帖样本。适配营销选题、品牌讨论分析、社媒舆情、PR 传播效果场景,覆盖头部消费品牌、热门事件、品类词。免费 200 次,无需注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermalo](https://clawhub.ai/user/supermalo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, PR, media buying, content operations, and research users can ask an agent to query Chinese social hot-search lists, analyze topic volume and sentiment, compare platform distribution, and sample representative posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social-media query terms and topic names are sent to a remote proxy.

Mitigation: Use only non-confidential topics unless the proxy operator and retention policy are acceptable for the work.

Risk: The skill creates a persistent local identity tied to a hash of the username and hostname.

Mitigation: Review local identity storage and avoid shared or sensitive environments where machine-linked usage tracking is not acceptable.

Risk: The agent configuration allows implicit invocation.

Mitigation: Require user confirmation before running queries that disclose sensitive topics or consume quota.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supermalo/skills/social-hotsearch)
- [Publisher profile](https://clawhub.ai/user/supermalo)
- [Social Skill Proxy MCP endpoint](https://47-103-200-210.nip.io/mcp)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Agent-facing guidance with shell commands and JSON tool results summarized into Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries remote social-media data through a proxy and may return hot-search items, topic metrics, platform distributions, sentiment data, and sampled posts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
