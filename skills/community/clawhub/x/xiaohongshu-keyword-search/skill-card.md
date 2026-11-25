## Description:

社媒平台小红书公开数据检索工具，关键词搜笔记、爆款选题、笔记详情、评论舆情、博主作品、粉丝获赞与收藏，输出 JSON，不登录不发布。触发词：小红薯、xhs、rednote、小红书、笔记链接、博主主页、竞品监控、KOL筛选、评论分析。用户要查小红书笔记、评论、选题、竞品或舆情时使用；抖音、快手、B站、微博、公众号不要用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

小红书创作者、运营团队和市场研究人员可用它按关键词、笔记链接或博主主页检索公开笔记、评论和创作者数据，支持选题、竞品与舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment was partial; runtime permissions were not verified, and some components had limited scanner coverage.

Mitigation: Review the skill’s permissions and local data handling before installation; treat the benign verdict as a limited assessment.

Risk: Successful results may be saved in temporary local logs, which can retain search queries and retrieved information.

Mitigation: Review temporary-log retention or set XHS_GUAIKEI_DISABLE_LOG=1 when local result logging is not wanted.

Risk: The skill sends search queries or links to the Guaikei service and uses GUAIKEI_API_TOKEN for access.

Mitigation: Avoid sending sensitive query terms or links, and keep the API token private.

## Reference(s):

- [参数说明](references/options.md)
- [故障排查](references/troubleshooting.md)
- [JSON 输出信封结构](assets/output_envelope.schema.json)
- [Guaikei 小红书数据服务](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/xiaohongshu-keyword-search)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [JSON envelope containing public notes, comments, creator data, and request/status metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One response envelope per command; result fields vary by search, detail, comment, or creator-post request.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
