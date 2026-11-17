## Description:

当用户需要做社媒内容日历研究、7 天或 30 天选题规划、发布时间观察、内容主题分组、平台节奏对比或运营素材整理时使用。覆盖小红书、抖音和快手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Social media marketers and content planners use this skill to review trends and examples across Xiaohongshu, Douyin, and Kuaishou, then organize 7- or 30-day topic calendars and platform-specific publishing plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it repeatedly uses an unpinned, changeable SocialDataX CLI package, creating supply-chain risk despite no clear evidence of malicious intent.

Mitigation: Use only if you accept the changing-package risk; review the package before running or choose a reviewed version.

Risk: Search topics may be sent to SocialDataX, so confidential subjects could be disclosed to the service.

Mitigation: Avoid confidential topics unless they are approved for sharing with SocialDataX.

Risk: The available security scan was partial and does not establish that every referenced component was inspected.

Mitigation: Review runtime-installed components before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-content-calendar-research)
- [SocialDataX skill and API key information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Markdown]

**Output Format:** [Structured JSON research results summarized in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rankings, popularity signals, sample titles, authors, links or content IDs, and pagination data.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
