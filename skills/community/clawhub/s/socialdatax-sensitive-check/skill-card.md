## Description:

用于敏感词检测、违禁词检测、文案发布前检查、内容安全检查、文案合规审核、能不能发判断、平台风险提示和改写建议。支持小红书、抖音、快手和通用文本场景，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media teams use this skill to review draft text for sensitive or prohibited terms before publishing on Xiaohongshu, Douyin, Kuaishou, or in general contexts, and to receive risk summaries and rewrite suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI runs an unpinned @latest package; a future release could change behavior or credential access, and the security scan was partial.

Mitigation: Use a package source you trust, consider which credentials are available to the CLI, and reassess the release before upgrading.

Risk: The service stores submitted text and structured results for history, billing, and troubleshooting.

Mitigation: Submit only text approved for processing by SocialDataX; avoid sending content that should remain private.

## Reference(s):

- [SocialDataX API key and service page](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-sensitive-check)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Structured JSON results, with concise summaries and rewrite suggestions suitable for Markdown presentation.]

**Output Parameters:** [1D text input; optional platform selector: generic, xhs, douyin, or kuaishou.]

**Other Properties Related to Output:** [Text-only in v1. The service stores submitted text and structured results for history, billing, and troubleshooting.]

## Skill Version(s):

0.1.15 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
