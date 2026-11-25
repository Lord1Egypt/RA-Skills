## Description:

当用户需要做今日头条内容研究、文章选题、热点角度整理或同主题内容对比时使用。输入主题或内容链接，基于相关作品和详情输出样本概览、标题模式与可继续验证的内容方向。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers and editors use this skill to examine Toutiao topics or posts, compare representative articles, identify title patterns, and develop follow-up angles grounded in retrieved samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release invokes the mutable socialdatax-skills@latest package, which carries supply-chain risk.

Mitigation: Review the package release and its behavior before installing or using it, especially when credentials are available.

Risk: Research topics or content links submitted for analysis may be sent to SocialDataX.

Mitigation: Avoid submitting confidential topics or links unless sharing them with SocialDataX is acceptable and authorized.

Risk: The security scan has partial coverage, so its assessment is incomplete.

Mitigation: Treat the security result as incomplete and review the release before relying on it.

## Reference(s):

- [SocialDataX AI skill information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/toutiao-content-research)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown with sample summaries, linked source items, title patterns, and follow-up angles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed sample scope and missing information when available; distinguishes engagement signals from analysis.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
