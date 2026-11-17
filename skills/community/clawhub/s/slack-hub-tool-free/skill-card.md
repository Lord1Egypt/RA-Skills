## Description: <br>
Slack Hub Tool Free helps an agent send Slack messages, reply in threads, search workspace content, and list public channels using a Slack bot token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and team members use this skill to ask an agent to send routine Slack messages, reply in existing threads, search prior workspace messages, and inspect available public channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Slack messages and search workspace content when configured with a bot token. <br>
Mitigation: Require explicit user confirmation before sending messages or running searches. <br>
Risk: Private-channel access may be possible if broad Slack scopes are granted. <br>
Mitigation: Limit the Slack app scopes to the needed functions and avoid groups:read unless private-channel access is intentional. <br>
Risk: Broad trigger wording may cause the skill to be invoked for communication tasks beyond the user's intent. <br>
Mitigation: Use the skill only for Slack message sending, thread replies, workspace search, and channel listing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/slack-hub-tool-free) <br>
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage) <br>
- [Slack search.messages API](https://slack.com/api/search.messages) <br>
- [Slack conversations.list API](https://slack.com/api/conversations.list) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-style response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Slack bot token; may send messages or search workspace content through Slack APIs.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
