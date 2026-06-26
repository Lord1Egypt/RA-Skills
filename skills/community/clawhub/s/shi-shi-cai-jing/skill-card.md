## Description: <br>
实时抓取并汇总新浪财经7×24小时全球财经新闻。通过API接口智能增量检测，每5分钟自动抓取最新新闻。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ripplefox](https://clawhub.ai/user/ripplefox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch, store, and summarize recent Sina Finance 7x24 global finance news with incremental update detection. It supports scheduled polling and local JSON state for avoiding duplicate news items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles a helper that can attach to a local browser debugging session. <br>
Mitigation: Prefer the documented fetch_api.js API path and avoid running fetch_and_save.js unless a dedicated browser debugging session was intentionally started for this skill. <br>
Risk: Five-minute scheduled polling can continue fetching external finance news if left enabled. <br>
Mitigation: Review any cron or scheduled task configuration before deployment and ensure operators can disable the polling job. <br>
Risk: The server security verdict is suspicious because the advertised API-only workflow differs from bundled browser-attachment behavior. <br>
Mitigation: Review the scripts before installation and require the publisher to remove, document, or gate the browser helper before broader use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ripplefox/shi-shi-cai-jing) <br>
- [Sina Finance news API endpoint](https://app.cj.sina.com.cn/api/news/pc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JavaScript scripts, shell commands, and JSON state/data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores fetched news in data/news_db.json, tracks incremental state in data/state.json, and groups summaries into finance-news categories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
