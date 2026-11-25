## Description:

通过关键词或链接查询小红书公开笔记、评论、博主作品与互动数据，并返回 JSON，供选题、竞品、KOL 和舆情分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

创作者、运营人员、品牌团队和内容分析人员可用此技能检索小红书公开笔记、评论及博主互动数据，用于内容选题、竞品跟踪、KOL 筛选和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags concerns about undeclared tool scope and data handling, and notes that some executable files were only partially inspected; this does not establish malicious intent.

Mitigation: Review the commands and information sent to the third-party service before use, and avoid sending sensitive keywords, links, or request data.

## Reference(s):

- [参数与查询限制](references/options.md)
- [意图路由](references/routing.md)
- [JSON 输出契约](references/contract.md)
- [错误处理](references/errors.md)
- [服务网站](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON response envelope containing public note, comment, or creator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches require a keyword; detail, comment, and creator queries require a matching public link or identifier. Results cover publicly visible data only.]

## Skill Version(s):

1.2.4 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
