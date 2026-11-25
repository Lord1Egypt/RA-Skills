## Description:

使用用户指定的 Easy WebBridge 浏览器与 1–3 篇公开公众号文章 URL，围绕关注问题提炼主结论、关键步骤、作者、日期和来源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to read one to three public WeChat articles in a user-selected browser and produce a source-linked brief based on visible page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented package installation command uses an unpinned external installer.

Mitigation: Review the package contents and installer source before running it, and use a specific reviewed release where available.

Risk: Optional draft editing can change content beyond the article-reading task.

Mitigation: Keep draft_fill_authorized false by default; only fill draft fields after the user explicitly authorizes the proposed content.

Risk: The security scan was partial: one script was only partly inspected and binary images were outside its scope.

Mitigation: Review the remaining script and binary assets or obtain a complete scan before relying on the security assessment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xxjrq/skills/wechat-article-reading-brief-free)
- [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge on Gitee](https://gitee.com/xxjrq/easy-webbridge)
- [OpenCLI WeChat browser adapter reference](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reading brief with article summaries, source URLs, and visible-content limitations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers 1–3 public article URLs for a short article, section, or single scenario; tables are limited to 100 rows.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
