## Description:

实时抓取并汇总新浪财经7×24小时全球财经新闻。通过API接口智能增量检测，每5分钟自动抓取最新新闻。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ripplefox](https://clawhub.ai/user/ripplefox)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch Sina Finance 7x24 market news, keep a local seven-day JSON news store current, and summarize updates by international events, domestic news, markets, and energy or commodities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retains fetched finance news locally and recurring cron use can create repeated local writes.

Mitigation: Enable the cron schedule only after confirming recurring local retention is desired, and review the generated data/news_db.json and data/state.json files during operation.

Risk: The artifact includes a browser automation script that can connect to an existing local browser session.

Mitigation: Use the documented fetch_api.js workflow for collection and avoid running fetch_and_save.js unless it is changed to use an isolated browser and fail closed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ripplefox/skills/shi-shi-cai-jing)
- [Sina Finance news API endpoint](https://app.cj.sina.com.cn/api/news/pc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and local JSON news records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches incremental Sina Finance items, stores seven days of data, and may run on a five-minute cron schedule.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
