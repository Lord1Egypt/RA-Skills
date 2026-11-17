## Description:

Public opinion monitoring and structured report generation that collects publicly available web information about celebrities, TV shows, or brands, performs sentiment analysis, and generates responsive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubinghuang2019-source](https://clawhub.ai/user/wubinghuang2019-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor public sentiment for public-facing entities and produce an evidence-based HTML report with sentiment distribution, event timelines, risk assessment, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches public web content and writes a local HTML report.

Mitigation: Confirm the target entity, time range, and desired report generation before invocation; use only publicly visible sources.

Risk: Public web sources may not expose precise platform metrics such as views, followers, or engagement counts.

Mitigation: Report only explicitly displayed metrics and label missing values as Data Unavailable instead of estimating them.

Risk: The default report template uses Chinese locale HTML conventions.

Mitigation: Adjust the report language and locale when the user requests a different audience or format.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubinghuang2019-source/skills/sentiment-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Self-contained HTML report with embedded CSS, plus agent guidance for public web research and report delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires web search, web fetch, and local file writing tools; reports missing public metrics as Data Unavailable.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
