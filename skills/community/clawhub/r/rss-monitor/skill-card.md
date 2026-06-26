## Description: <br>
Monitor RSS feeds and send notifications when new content is published. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lwd815813](https://clawhub.ai/user/lwd815813) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to monitor RSS, Atom, and JSON feeds for new articles, optionally send Feishu/Lark notifications, and schedule recurring feed checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured feed URLs and recent article history are stored locally under ~/.rss_monitor. <br>
Mitigation: Use non-sensitive feed sources where possible and review or remove the local state files when monitoring is no longer needed. <br>
Risk: Optional Feishu/Lark notifications can disclose article titles to an external chat service. <br>
Mitigation: Keep the webhook URL private and avoid routing sensitive feed notifications to shared external channels. <br>
Risk: Scheduled monitoring can continue fetching feeds after the user no longer expects it. <br>
Mitigation: Remove related cron or OpenClaw cron entries when ongoing checks are no longer required. <br>


## Reference(s): <br>
- [RSS Monitor ClawHub release page](https://clawhub.ai/lwd815813/rss-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes monitored feed state and article history as local JSON files under ~/.rss_monitor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
