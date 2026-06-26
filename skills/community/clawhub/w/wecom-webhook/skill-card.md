## Description: <br>
Sends Enterprise WeChat group notifications as text or Markdown through a configured webhook, with examples for immediate and scheduled reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiekch](https://clawhub.ai/user/xiekch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send Enterprise WeChat group alerts, reminders, and Markdown status updates from an agent or scheduled OpenClaw cron task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook keys can authorize messages to an Enterprise WeChat group if exposed. <br>
Mitigation: Treat the webhook key like a password, avoid sharing it, and rotate the Enterprise WeChat group bot webhook if it is leaked. <br>
Risk: Scheduled reminders may send unwanted or sensitive content if configured incorrectly. <br>
Mitigation: Test with harmless content first, avoid secrets or sensitive personal data in scheduled messages, and remove cron jobs that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiekch/wecom-webhook) <br>
- [Publisher profile](https://clawhub.ai/user/xiekch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces webhook request guidance and shell commands; runtime sends outbound Enterprise WeChat webhook messages.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
