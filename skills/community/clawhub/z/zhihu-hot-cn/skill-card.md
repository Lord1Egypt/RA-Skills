## Description:

知乎热榜监控 - 获取知乎热门话题、问题和趋势分析（Quora 中国版）

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content teams can use this skill to fetch Zhihu hot-list topics from public data sources and format them for trend review, content planning, or market monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches mutable public data from GitHub, so results can change independently of the skill release.

Mitigation: Review fetched data before using it in decisions or downstream automation.

Risk: The security guidance notes that JSON output should not be used for security-sensitive automation without stronger escaping and input validation.

Mitigation: Add proper JSON escaping and input validation before consuming the output in security-sensitive workflows.

Risk: The security summary notes some overstated documentation, so advertised behavior may exceed the implemented script.

Mitigation: Validate required options against the shipped artifact before relying on them in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/zhihu-hot-cn)
- [zhihu-hot-questions](https://github.com/towelong/zhihu-hot-questions)
- [SnailDev/zhihu-hot-hub](https://github.com/SnailDev/zhihu-hot-hub)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown, JSON, or simple text hot-list output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches mutable public GitHub-hosted source data and formats it locally.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
