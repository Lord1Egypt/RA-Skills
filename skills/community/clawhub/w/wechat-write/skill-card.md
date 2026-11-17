## Description:

公众号文案创作工具。基于红狐数据公众号爆款雷达每日收录的热门文章，按关键词检索爆款、分析流量规律、生成可发布的完整文章。当用户写公众号文章、生成公众号文案、查找爆款文章、分析爆款规律时使用。触发词：公众号文案、公众号爆款、爆款文章、公众号写作、公众号文章生成。当接口返回积分不足（code=3210）时，自动唤起支付宝完成充值后继续查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat Official Account writers use this skill to find trending articles by keyword, study engagement patterns, and draft a publishable Chinese article with suggested titles and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recharge workflow may install payment software and initiate a recharge when a query lacks credits.

Mitigation: Review the recharge workflow; require approval before installing payment software and before each recharge; verify the merchant and amount; use a reviewed, fixed software version.

Risk: Search keywords are sent to RedFox and may reveal sensitive topics.

Mitigation: Do not submit confidential or sensitive search terms.

## Reference(s):

- [Alipay recharge workflow](artifact/references/alipay-recharge.md)
- [Trend data format](artifact/references/gzh_trend_data_format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Chinese Markdown with article titles, a publishable article, tags, trend analysis, and source-article links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually includes 3–6 title suggestions, an approximately 1,500-character article, and 5–10 tags.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
