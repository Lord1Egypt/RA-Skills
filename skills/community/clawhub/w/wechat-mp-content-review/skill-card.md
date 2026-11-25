## Description:

当用户提供公众号文章链接、账号 ID 或明确的文章名单，需要公众号内容复盘、近期推文对比、题材表现分析或读者反馈整理时使用。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

公众号运营者可用此技能对指定文章或账号近期文章进行内容复盘，比较可见互动数据、整理读者反馈，并形成下一轮选题建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples use the changeable socialdatax-skills@latest package, which creates a supply chain risk around configured credentials.

Mitigation: Review the package and pin a trusted version before use, especially in environments containing credentials or sensitive files.

Risk: The security scan was partial because two local references could not be resolved, so the available security evidence is incomplete.

Mitigation: Resolve the missing references and complete a security review before relying on the scan as comprehensive.

## Reference(s):

- [SocialDataX AI and API key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/wechat-mp-content-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with comparison tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed data and gaps; samples at most 10 articles across up to 3 pages and provides up to 3 recommendations.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
