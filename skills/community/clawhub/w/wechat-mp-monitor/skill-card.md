## Description: <br>
Monitor WeChat MP articles and send notifications for public account updates, article summaries, and new-content alerts through optional Feishu/Lark delivery and scheduled checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lwd815813](https://clawhub.ai/user/lwd815813) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to track WeChat public account updates, summarize individual article URLs, maintain a watchlist, and configure Feishu/Lark notifications for monitored content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches article URLs provided by the user and stores watchlist and article history data under ~/.wechat_mp_monitor. <br>
Mitigation: Review the accounts and URLs being monitored, and remove the local data directory when monitoring is no longer needed. <br>
Risk: Feishu/Lark webhook URLs and notification content may be exposed if webhook URLs are saved in the watchlist or shared with an unintended endpoint. <br>
Mitigation: Prefer the FEISHU_WEBHOOK environment variable, treat webhook URLs as secrets, and review notification content before enabling delivery. <br>
Risk: Scheduled monitoring can continue running after setup through cron or OpenClaw cron. <br>
Mitigation: Remove the cron entry when monitoring should stop. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lwd815813/wechat-mp-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print article summaries, watchlist status, history entries, and notification status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
