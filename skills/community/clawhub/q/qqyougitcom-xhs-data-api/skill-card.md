## Description:

深度解读小红书CES算法和流量池机制，分析爆款笔记规律、竞品策略、标题公式、标签组合和运营提升计划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, brand operators, and social-commerce analysts use this skill to analyze public Xiaohongshu notes, creators, competitors, market topics, and performance benchmarks. It supports data-informed content strategy, collaboration screening, competitive review, and 30-day operations planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis prompts and related marketing context may be sent to the skill provider's Xiaohongshu data API using XHS_API_KEY.

Mitigation: Avoid submitting confidential campaign plans, private account data, or sensitive competitor research unless the provider's data handling is acceptable.

Risk: Xiaohongshu algorithm behavior and category benchmarks can change over time.

Mitigation: Treat recommendations as current guidance, refresh benchmarks regularly, and review outputs against recent public platform data.

Risk: Provider API responses may include coverage limits or data gaps.

Mitigation: Surface coverage notes and data-gap fields in user-facing analysis before making operational decisions.

## Reference(s):

- [小红书数据分析 Skill](https://clawhub.ai/qqyougitcom/skills/qqyougitcom-xhs-data-api)
- [聚合接口完整参考](references/aggregate-api.md)
- [xhs-data-api 详细参考 v1.3.0](references/details.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Chinese Markdown analysis with API-backed findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XHS_API_KEY for provider API access; API-backed outputs should include coverage notes and data gaps when present.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
