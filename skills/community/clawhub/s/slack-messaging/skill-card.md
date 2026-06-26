## Description: <br>
Slack messaging for sending messages, managing channels, uploading files, adding reactions, and automating team notifications through Slack Web API commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to prepare Slack API calls for workspace messaging, channel administration, file sharing, reactions, user lookup, and notification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Slack token can let an agent post, read, upload files, react, and look up users within the scopes and channels granted to that token. <br>
Mitigation: Use a low-privilege bot token limited to the specific scopes and channels needed for the task. <br>
Risk: Messaging, channel, and file actions can disclose sensitive information or send content to the wrong Slack destination. <br>
Mitigation: Confirm channel IDs, user IDs, recipients, and message content before write actions, and do not post secrets, customer data, private logs, or sensitive incident details unless workspace policy allows it. <br>
Risk: High-volume automation can exceed Slack rate limits and cause failed or delayed notifications. <br>
Mitigation: Respect Slack rate limits and Retry-After headers when generating or running repeated API calls. <br>


## Reference(s): <br>
- [Slack API Apps](https://api.slack.com/apps) <br>
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage) <br>
- [Slack conversations.list API](https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=200) <br>
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Slack Web API examples require a SLACK_TOKEN and caller-supplied channel, user, timestamp, file, and message values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
