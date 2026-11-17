## Description:

零配置即装即用，支持火车票查询含12306实时余票、去火车站交通方式查询和住宿推荐，多旅游平台数据直连。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel assistants use this skill to query China train schedules, prices, live 12306 seat availability, station transportation options, and hotel recommendations with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel routes, station addresses, dates, and hotel preferences are sent to external China travel and mapping services through publisher proxy endpoints.

Mitigation: Use the skill only when this data sharing is acceptable, and treat PROXY_TOKEN as an authentication secret when configured.

Risk: Ticket availability, prices, booking links, and route estimates can change or depend on upstream service availability.

Mitigation: Confirm ticket details on the final booking page and use map or carrier sources for time-sensitive travel decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/travel-skills/skills/train-ticket-query)
- [12306 station-name data endpoint](https://kyfw.12306.cn/otn/resources/js/framework/station_name.js)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted Chinese text with links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns train options, live-seat notes, route estimates, hotel recommendations, status messages, and external booking links.]

## Skill Version(s):

1.1.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
