## Description: <br>
Sends text or Markdown notifications to Enterprise WeChat groups through a webhook, with optional user and mobile mentions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiekch](https://clawhub.ai/user/xiekch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send immediate or scheduled Enterprise WeChat group reminders, task notifications, and status updates through a configured webhook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook keys can expose the Enterprise WeChat group notification channel if shared or logged. <br>
Mitigation: Keep webhook keys private, rotate any leaked key, and avoid placing secrets in shared logs or visible scheduled task text. <br>
Risk: Notification content may expose sensitive information through command history, logs, or scheduled reminder definitions. <br>
Mitigation: Review message content and scheduled tasks before use, and avoid sending confidential data through group notifications. <br>
Risk: Broad mentions such as @all can notify more people than intended. <br>
Mitigation: Use targeted user IDs or mobile mentions when possible and review cron reminders after creating them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiekch/weixin-webhook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown usage guidance with bash commands and JSON message examples; webhook calls return response text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text and markdown message modes, optional mentioned user IDs, optional mentioned mobile numbers, and scheduled reminder examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
