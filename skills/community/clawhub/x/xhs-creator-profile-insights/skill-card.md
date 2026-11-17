## Description:

当用户需要做小红书博主画像、小红书博主信息、账号资料、创作者定位、粉丝规模判断或合作对象初筛时使用。面向品牌、MCN、内容运营和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向品牌、MCN、内容运营和创作者，用于根据小红书账号主页、分享文本或账号 ID 获取创作者资料，并支持合作对象初筛与后续分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI command downloads an unpinned package release that can change over time; the security scan warns a future compromised release could expose credentials or local data.

Mitigation: Review the package source and version before running it, prefer a pinned reviewed version when possible, and provide only credentials or data you are comfortable using with it.

Risk: Profile information submitted for lookup is sent to SocialDataX.

Mitigation: Use only profile identifiers and information you are permitted to share, and avoid submitting sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/xhs-creator-profile-insights)
- [SocialDataX API key and skill information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Markdown creator profile summary with profile facts and follow-up angles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates visible profile facts from strategic judgments.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
