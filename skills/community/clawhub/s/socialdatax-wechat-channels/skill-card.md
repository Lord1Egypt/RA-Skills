## Description:

用于视频号数据助手、视频号热榜、内容研究、作品详情、评论分析、创作者资料和作品列表，也支持微信公众号文章链接详情和互动统计。覆盖 WeChat Channels，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容研究人员、创作者和社媒团队可用它查询视频号热榜、内容详情、评论与创作者资料，并查看微信公众号文章详情和互动统计。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI is installed from an unpinned latest release, so its behavior may change between runs.

Mitigation: Review package changes and use a vetted pinned release when reproducibility or change control matters.

Risk: Submitted links or share text may be sent to SocialDataX without clear disclosure.

Mitigation: Avoid sending private or token-bearing content, and submit links or text only when authorized for external processing.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-wechat-channels)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text, JSON]

**Output Format:** [Structured query results with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only data lookups for WeChat Channels and WeChat Official Account content.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
