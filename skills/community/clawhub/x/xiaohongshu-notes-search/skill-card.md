## Description:

小红书高赞笔记搜索工具。支持关键词获取小红书实时高赞（高收藏、高评论）笔记数据，助力创作者发现热门趋势、获取创作灵感。支持四大能力：(1) 关键词搜索笔记/视频，可按点赞数、评论数、收藏数、发布时间、内容类型筛选排序；(2) 博主作品抓取，按主页链接获取博主的互动数据（粉丝量、点赞量或收藏量等）或公开作品列表；(3) 笔记（视频）详情，获取详情数据及互动数据等，分析笔记的市场表现；(4) 笔记评论分析，按笔记链接获取评论内容与互动数据。用户提到小红书/xhs/rednote 且需要查数据、市场调研、舆情监测、做选题、竞品监控、KOL筛选、舆情分析时调用；无需登录账号

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketing teams, and analysts use the skill to search public Xiaohongshu notes, review creator profiles, inspect note details and comments, and support topic research, competitor monitoring, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence marks the release suspicious with medium confidence, citing unclear tool scope, a privacy concern in support guidance, and partial review of 13 of 42 components.

Mitigation: Review the declared tool scope and data-sharing details before installing; provide only public Xiaohongshu query terms or links you are comfortable sending to Guaikei.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/xiaohongshu-notes-search)
- [Guaikei service and API access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Output contract](references/contract.md)

## Skill Output:

**Output Type(s):** [JSON data, Public Xiaohongshu research data]

**Output Format:** [Structured JSON envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; requires Node.js 16.14+ and GUAIKEI_API_TOKEN. Query keywords and links are sent to Guaikei; local files are not uploaded.]

## Skill Version(s):

1.2.2 (source: evidence.release.version, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
