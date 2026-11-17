## Description:

分析小红书各垂类行业笔记或视频和达人趋势，输出市场机会与风险。当用户询问小红书市场规模、类目增长或达人结构时使用。支持四大能力：(1) 关键词搜索笔记/视频，可按点赞数、评论数、收藏数、发布时间、内容类型筛选排序；(2) 博主作品抓取，按主页链接获取博主的互动数据（粉丝量、点赞量或收藏量等）或公开作品列表；(3) 笔记（视频）详情，获取详情数据及互动数据等，分析笔记的市场表现；(4) 笔记评论分析，按笔记链接获取评论内容与互动数据。用户提到小红书/xhs/rednote 且需要查数据、市场调研、做选题、竞品监控、KOL筛选、舆情分析时调用；无需登录账号

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External marketers, content operators, data analysts, and agent workflow builders use this skill to retrieve public Xiaohongshu keyword, note, creator, and comment data for trend research, competitor monitoring, KOL screening, sentiment analysis, and report drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided Xiaohongshu keywords or links and the GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use the skill only when third-party API processing is acceptable, keep the token in environment variables, and avoid submitting links or queries that should not leave the local environment.

Risk: Returned public-data results, xsec_token-containing URLs, comment data, and profile datasets may be saved in local logs.

Mitigation: Treat local logs and exported results as sensitive working data, limit sharing, and remove logs according to team retention policy.

Risk: Large limits can create bulky result sets and increase rate-limit or exposure risk.

Mitigation: Start with focused limits, increase only when needed for analysis, and reduce frequency or retry later after 429 responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/why20261/skills/xiaohongshu-market-insight)
- [Project Homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Guaikei API Token Site](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Troubleshooting Reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [Issue Tracker](https://github.com/um-why/xiaohongshu-openclaw-skill/issues)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands can return up to 10000 public-data records and may write local logs.]

## Skill Version(s):

1.1.4 (source: SKILL.md frontmatter, package.json, evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
