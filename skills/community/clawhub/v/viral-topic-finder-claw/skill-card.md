## Description:

全网热点实时监控与爆款选题挖掘技能，用于抓取微博、抖音、知乎、百度和 B 站等平台热榜，过滤账号相关热点，分析爆款内容规律，并生成可执行选题建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and marketing teams use this skill to discover current Chinese-platform hot topics, match them to an account positioning strategy, and turn them into structured topic recommendations or optional Feishu topic-library records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie-based platform access may expose live browser credentials if users paste cookies into tracked source files.

Mitigation: Prefer public read-only endpoints; when cookies are necessary, use a dedicated low-privilege account and store secrets outside source code.

Risk: Automatically generated topic recommendations may preserve incorrect or unsuitable hot-topic framing for a user's account.

Mitigation: Review recommendations against account positioning, excluded keywords, and final editorial judgment before publishing or archiving.

Risk: Optional Feishu writes may store topic, account, or competitive-analysis data that the user did not intend to retain.

Mitigation: Confirm the target Feishu table and the fields to be written before creating records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/viral-topic-finder-claw)
- [平台热榜数据抓取指南](references/platform-hotlist-api.md)
- [爆款内容分析模型](references/viral-content-analysis.md)
- [账号定位关键词库](references/account-keywords.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured topic cards and optional shell commands or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hotlist summaries, title alternatives, content angles, emotional triggers, timing windows, traffic-potential estimates, production-difficulty estimates, and optional Feishu table fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
