## Description:

一站式小红书运营工具，融合选题灵感、数据分析模块。支持爆款标题、热点选题、粉丝分析等，覆盖小红书运营数据获取场景。支持关键词搜索笔记和视频、抓取博主作品、查询笔记详情及分析评论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and social media teams can search public Xiaohongshu posts, inspect creator and post metrics, and review comments to support topic research, competitor monitoring, creator screening, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and supplied links are sent to guaikei.com with the service token, and use may incur charges.

Mitigation: Review the provider's pricing and data practices before making requests.

Risk: Query and result files are retained locally by default.

Mitigation: Set XHS_GUAIKEI_DISABLE_LOG=1 to disable local logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-yunying-zhushou)
- [Guaikei service](https://www.guaikei.com)
- [options.md](references/options.md)
- [troubleshooting.md](references/troubleshooting.md)
- [changelog.md](references/changelog.md)
- [GitHub Issues](https://github.com/um-why/xiaohongshu-openclaw-skill/issues)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON envelope containing Xiaohongshu search results, post details, comments, creator metrics, and request metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Engagement counts are returned as strings; results cover public content.]

## Skill Version(s):

1.2.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
