## Description:

Slack Hub Skill lets an agent send Slack messages, reply in threads, search workspace content, and list channels through a configured Slack bot token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icyfrosty](https://clawhub.ai/user/icyfrosty)

### License/Terms of Use:


## Use Case:

Developers and operators can use this skill to connect an agent to Slack for workspace messaging, threaded replies, message/file search, and channel listing. It is intended for Slack workspaces where bot-token access and search results are acceptable for the agent's role.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The channel-listing action may request private-channel metadata even though the skill documentation describes public-channel listing.

Mitigation: Avoid the list action unless private-channel metadata exposure is acceptable, and restrict the Slack bot token to the narrowest scopes and channel memberships possible.

Risk: Send and search actions can expose or distribute sensitive Slack content.

Mitigation: Verify message targets and content before sending, and share search results only with audiences authorized to see the underlying Slack data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icyfrosty/skills/slack-hub-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/icyfrosty)
- [Slack chat.postMessage API endpoint](https://slack.com/api/chat.postMessage)
- [Slack search.messages API endpoint](https://slack.com/api/search.messages)
- [Slack conversations.list API endpoint](https://slack.com/api/conversations.list)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Shell commands, Configuration]

**Output Format:** [JSON-formatted Slack API responses and Slack message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May expose sensitive Slack message, file, channel, or private-channel metadata depending on token scopes and channel memberships.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact skill.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
