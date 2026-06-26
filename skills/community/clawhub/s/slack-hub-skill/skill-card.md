## Description: <br>
Slack Hub Skill lets an agent send Slack messages, reply in threads, search workspace content, and list channels through a Slack bot token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IcyFrosty](https://clawhub.ai/user/IcyFrosty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace automation agents use this skill to post messages, reply to Slack threads, search workspace content, and inspect channel availability from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post messages to Slack channels or users using the configured bot token. <br>
Mitigation: Require confirmation of destination, message text, and thread context before sending messages. <br>
Risk: The skill can search workspace content and may expose sensitive messages available to the bot token. <br>
Mitigation: Use the narrowest Slack scopes possible and avoid tokens with unnecessary private-channel or broad search access. <br>
Risk: The skill can list channel metadata under the bot token's permissions. <br>
Mitigation: Limit bot workspace access and review channel-listing results before using them in downstream automation. <br>


## Reference(s): <br>
- [ClawHub Slack Hub Skill](https://clawhub.ai/IcyFrosty/slack-hub-skill) <br>
- [IcyFrosty publisher profile](https://clawhub.ai/user/IcyFrosty) <br>
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage) <br>
- [Slack search.messages API](https://slack.com/api/search.messages) <br>
- [Slack conversations.list API](https://slack.com/api/conversations.list) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON API responses and CLI text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Slack bot token in SLACK_BOT_TOKEN and network access to Slack APIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
