## Description: <br>
Send messages, manage channels, handle files, and coordinate team communication in Slack via the Slack API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, workspace administrators, and developers use this skill to automate Slack communication, search workspace information, manage channels and files, create reminders, and coordinate team workflows from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a connected Slack OAuth workspace and can access Slack data according to the granted permissions. <br>
Mitigation: Install only when the publisher and ClawLink connection are trusted, and grant only the Slack permissions needed for the intended workspace tasks. <br>
Risk: Write operations can send messages, change channels, upload or delete files, invite users, or make other visible workspace changes. <br>
Mitigation: Require a preview of the exact target and effect, then get explicit user approval before executing any write or destructive action. <br>
Risk: Ambiguous channel, user, file, or tool selection can affect the wrong Slack resource. <br>
Mitigation: Resolve names to Slack IDs with read/search tools and use tool descriptions or previews before calling write tools. <br>
Risk: Slack API rate limits can delay or fail list and history operations. <br>
Mitigation: Honor Slack rate-limit responses, including Retry-After guidance, and avoid unnecessary repeated calls. <br>


## Reference(s): <br>
- [Slack API Documentation](https://api.slack.com/) <br>
- [Slack Web API Reference](https://api.slack.com/methods) <br>
- [Slack Rate Limits](https://api.slack.com/docs/rate-limits) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/slack-workspace) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Slack and ClawLink tool names, connection checks, previews, and confirmation steps before write operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
