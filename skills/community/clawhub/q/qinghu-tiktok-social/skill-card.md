## Description:

青虎AI TikTok 社媒运营：监控 TikTok 行业热门话题与视频榜单，按关键词搜索高赞内容，批量查视频详情并读评论，拆解脚本结构、播放爆发力与互动亮点，持续为短视频创作提供选题与拍摄灵感。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and content teams use this skill to research TikTok topic trends, video rankings, peer-account activity, and comment signals, then turn the findings into actionable short-video content ideas and calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Qinghu API token and sends TikTok research queries to Qinghu's API.

Mitigation: Use an appropriate token for the task, avoid sharing unrelated secrets, and confirm API calls before execution.

Risk: Larger result sets may be exported to local files.

Mitigation: Review exported files for sensitive or unnecessary data and delete them when they are no longer needed.

Risk: Trend and comment analysis can become stale or misleading if the data period, region, or sample size is unclear.

Mitigation: State the region, period, and sample size with conclusions, and avoid mixing regions or periods in comparisons.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-tiktok-social)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, files, guidance]

**Output Format:** [Markdown summaries with concise recommendations, optional exported table files for larger result sets, and JSON-over-HTTP API call examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data period, region, sample size, Qinghu credit usage when API calls are made, and local export links when larger records are saved.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
