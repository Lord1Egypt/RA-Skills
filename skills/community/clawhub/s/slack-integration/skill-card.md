## Description:

Send messages, upload files, list channels, query users, manage scheduled messages, search messages, and set bot status in Slack using the Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaolfun](https://clawhub.ai/user/gaolfun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to let an agent perform Slack Web API operations in a configured Slack workspace, including posting messages, listing channels, looking up users, uploading files, scheduling messages, searching messages, and setting bot status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad Slack posting, searching, user lookup, and file upload actions.

Mitigation: Grant only the Slack scopes needed for the intended workflow and require explicit confirmation before posting, deleting scheduled messages, searching messages, or uploading files.

Risk: Slack bot tokens are sensitive secrets that can authorize workspace actions if exposed.

Mitigation: Store bot tokens only in secure environment or secret configuration, keep them out of prompts, logs, screenshots, and shared documents, and revoke or regenerate any exposed token.

Risk: Search and user lookup capabilities can expose private workspace information available to the bot.

Mitigation: Avoid broad search and read scopes unless necessary, limit bot channel membership, and review search results before sharing them outside the requesting context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaolfun/skills/slack-integration)
- [Slack Apps](https://api.slack.com/apps)
- [Slack Web API](https://api.slack.com/web)
- [Slack Block Kit](https://api.slack.com/block-kit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Slack API request examples and status or error summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Slack API calls, curl examples, channel and user identifiers, file references, timestamps, and remediation guidance for Slack API errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
