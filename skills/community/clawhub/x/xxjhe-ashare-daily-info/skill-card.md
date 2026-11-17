## Description:

股票机构消息日报筛选工具，从指定API信源获取当日机构研报和资讯，按影响力、重要性、新颖性等维度评分筛选，输出Top 20精选日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[raisonliu](https://clawhub.ai/user/raisonliu)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and quantitative researchers use this skill to fetch the current A-share institutional-news feed, filter items by timeliness, impact, importance, evidence quality, and novelty, and produce a concise Top 20 daily Markdown report for market monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports rely on a single unauthenticated third-party HTTP feed from a bare IP address.

Mitigation: Treat generated reports as unverified market information and verify important claims against primary filings or trusted financial-news sources.

Risk: Market-news summaries may be mistaken for investment advice.

Mitigation: Use the output for research and monitoring only, and require independent financial judgment before taking investment action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raisonliu/skills/xxjhe-ashare-daily-info)
- [Publisher profile](https://clawhub.ai/user/raisonliu)
- [Configured daily information feed](http://81.68.131.238/api/today)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily report with ranked news items and a brief theme summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top 20 selected items; intermediate scoring is not included in the final output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
