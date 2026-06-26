## Description: <br>
Automate Slack messaging, channels, and search with Block Kit. Use when sending scheduled messages, syncing channels, monitoring chats, notifying teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and team members use this skill to send Slack webhook messages, create reusable notification templates, track local send history, and prepare scheduled team alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted message or configuration text can cause local code execution in the script. <br>
Mitigation: Do not use this version with untrusted or copied message text; review commands and configuration before running the skill. <br>
Risk: Slack webhook URLs, message history, templates, schedules, and exports are stored as sensitive local files. <br>
Mitigation: Keep the webhook scoped to the least sensitive Slack channel, protect ~/.slack-automator files, and rotate any webhook URL that may have been exposed. <br>


## Reference(s): <br>
- [Slack App Configuration](https://api.slack.com/apps) <br>
- [BytesAgain](https://bytesagain.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/slack-automator) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Slack webhook payloads and stores local configuration, templates, schedules, history, and exports under ~/.slack-automator.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
