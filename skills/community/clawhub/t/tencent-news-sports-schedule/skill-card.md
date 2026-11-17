## Description:

当用户查询某项体育赛事或某支球队的赛程、下一场比赛、比赛时间、对阵、比分、直播链接或支持的赛事列表时使用。通过腾讯新闻 CLI 查询已接入的赛事；实际覆盖范围以当次赛事列表为准。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Sports fans use this skill to check currently supported competitions and retrieve schedules, fixtures, scores, and live links for a competition or team. It presents only data returned by the current query and distinguishes incomplete or failed queries from an absence of matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded scripts, and troubleshooting may encourage bypassing security protections.

Mitigation: Review recovery instructions, use a verified CLI release, explicitly approve installation or update changes, keep security protections enabled, consult an administrator about enterprise blocks, and enter API keys only in a local terminal.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tencent-adm/skills/tencent-news-sports-schedule)
- [Publisher profile](https://clawhub.ai/user/tencent-adm)
- [Tencent News API Key page](https://news.qq.com/exchange?scene=appkey)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Concise text or Markdown lists/tables of matches, dates, scores, and returned live links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the selected competition, team, and date range and only include information returned by the CLI; dates are interpreted using Beijing time when specified by the request.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
