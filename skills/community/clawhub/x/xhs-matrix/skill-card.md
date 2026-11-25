## Description:

小红薯账号矩阵数据源（只读）：关键词搜笔记、爆款选题、笔记详情、评论舆情、博主作品、粉丝获赞与收藏，输出 JSON，不登录不发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、品牌运营与数据分析人员可用它检索小红书公开笔记、评论和博主数据，支持选题调研、竞品对比、KOL筛选与矩阵巡检。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and public Xiaohongshu links are sent to the Guaikei API.

Mitigation: Use public query inputs only and keep GUAIKEI_API_TOKEN in an environment variable.

Risk: ClawScan rated the skill benign with medium confidence, but scanner coverage was partial and 13 of 43 components could not be fully interpreted.

Mitigation: Review the source files before use and keep calls within the documented read-only public-data operations.

## Reference(s):

- [Guaikei Xiaohongshu data API](https://www.guaikei.com)
- [Parameter and calling guide](artifact/references/options.md)
- [Output contract](artifact/references/contract.md)
- [Troubleshooting guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON envelope with search, note, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The envelope distinguishes success, empty results, and errors; result shapes vary by command. Some interaction counts are strings, and successful or empty responses may include an estimated cost.]

## Skill Version(s):

1.2.3 (source: frontmatter, package.json, changelog, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
