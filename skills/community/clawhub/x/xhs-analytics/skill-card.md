## Description:

小红书数据分析工具，用于笔记搜索、博主分析、热度追踪、竞品对比和报告生成。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[legou20221023](https://clawhub.ai/user/legou20221023)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operators can use this skill to guide Xiaohongshu note search, author analysis, trend analysis, competitor comparison, and report generation workflows. The included scripts currently produce sample analytics unless the publisher documents and implements real data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure Xiaohongshu API keys or cookies before credential handling and network destinations are explicit.

Mitigation: Do not provide cookies or API keys until the publisher documents credential storage, handling, and network destinations; use sample, manual, or approved data sources instead.

Risk: The scripts mostly return sample analytics that could be mistaken for real Xiaohongshu data.

Mitigation: Clearly label sample outputs and validate generated reports against a documented live data source before making operational or commercial decisions.

Risk: Collection of platform data can create compliance and privacy issues if request rates, data scope, or third-party services are not controlled.

Mitigation: Follow Xiaohongshu platform rules, avoid collecting private personal information, and review any third-party data service before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legou20221023/skills/xhs-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON analytics output, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may write JSON, CSV, or Markdown files; outputs should be treated as sample data unless a real data source is configured and documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
