## Description:

用于敏感词检测、违禁词检测、文案发布前检查、内容安全检查、文案合规审核、能不能发判断、平台风险提示和改写建议。支持小红书、抖音、快手和通用文本场景，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要检查社交媒体文案的内容创作者和运营人员，用于发布前检查敏感或违禁表达、评估平台风险，并获取改写建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked the skill suspicious because it uses a mutable @latest CLI that may handle credentials or submitted text; the scan was partial and some local references could not be resolved.

Mitigation: Use a reviewed exact CLI version through a controlled, locked dependency workflow, and review the unresolved references before deployment.

Risk: The service stores submitted text and structured detection results for history, billing, and troubleshooting.

Mitigation: Submit only text approved for this service to process; avoid sending confidential or sensitive material.

## Reference(s):

- [SocialDataX AI and API key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-sensitive-check)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON findings summarized in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include violation status, risk level, matched types, highlighted excerpts, a summary, and rewrite suggestions.]

## Skill Version(s):

0.1.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
