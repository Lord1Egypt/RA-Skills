## Description: <br>
AI视频号信息源每日扫描微信视频号 AI 相关作品，按点赞、分享和评论筛选热门内容，并聚类生成本地 HTML 日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, AI creators, and industry observers use this skill to monitor AI-related WeChat Channels trends, rank posts by engagement, cluster topics, and generate a local daily report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subscription mode can persist REDFOX_API_KEY in a local scheduler file. <br>
Mitigation: Prefer one-off runs; if subscription is used, keep the local scheduler file protected and rotate or revoke the key after removal. <br>
Risk: Non-macOS subscription setup uses shell-based cron edits. <br>
Mitigation: Review the resulting crontab entry before relying on scheduled execution, and remove it with the unsubscribe flow or manual crontab editing when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/redfox-data/wechat-channels-ai-feed) <br>
- [RedFox API key settings](https://www.redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML files, shell commands, configuration guidance] <br>
**Output Format:** [Terminal text plus a local HTML daily report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; optional subscription can schedule local daily report generation at 16:00.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
