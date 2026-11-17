## Description:

公众号搜索工具，支持按关键词搜索爆款文章，展示推荐热门文章，助力内容创作者把握趋势与获取灵感；当用户需要搜索公众号文章、查找爆款内容、获取创作灵感时使用。当接口返回积分不足（code=3210）时，自动唤起支付宝完成充值后继续查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and publishing teams can find trending WeChat Official Account articles by keyword, review popular recommendations and ranking signals, and use the results for topic research and inspiration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insufficient provider credits can start a payment setup flow, and payment tooling may be installed if missing.

Mitigation: Keep recharge manual or require approval after verifying the payee and exact amount. Use a reviewed, pinned payment CLI and approve installation before proceeding.

Risk: Optional HTML reports may contain unsafe markup or links.

Mitigation: Prefer JSON output; review HTML and validate escaping and links before opening or sharing it.

Risk: Searches consume provider credits, and recurring delivery can create ongoing activity.

Mitigation: Confirm the intended query and credit use; enable recurring delivery only when requested.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/redfox-data/skills/wechat-explosive-content)
- [Article result format](references/gzh_trend_data_format.md)
- [Recharge flow reference](references/alipay-recharge.md)
- [RedFox API key setup](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML reports]

**Output Format:** [JSON search results or an optional HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include ranked articles and may include popular-topic recommendations; HTML output is saved as a local file.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
