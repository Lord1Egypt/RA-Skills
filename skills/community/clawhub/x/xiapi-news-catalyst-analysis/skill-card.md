## Description:

基于 daxiapi-cli news 命令，对 A 股个股舆情、公告和研报进行信息收集、噪音过滤、信源分级、影响评分，并生成结构化消息面跟踪报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to assess recent A-share stock-news catalysts by combining sentiment items, exchange announcements, and research reports into a concise, evidence-traceable report. It is intended for stock-specific news and catalyst analysis, not technical-indicator teaching or non-A-share markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs a mutable npm CLI with token access.

Mitigation: Pin a reviewed daxiapi-cli version, use a minimally scoped revocable DaxiAPI token, avoid exposing token values in chat or logs, and run the CLI in a restricted environment.

Risk: Stock-news conclusions can be distorted by noisy sentiment items, stale events, or overconfident scoring.

Mitigation: Apply the documented noise filtering, source ranking, recency scoring, and disclaimer requirements; treat generated reports as reference material rather than investment advice.

## Reference(s):

- [Report template](assets/report-template.md)
- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-news-catalyst-analysis)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured DaxiAPI token and a confirmed A-share stock code.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
