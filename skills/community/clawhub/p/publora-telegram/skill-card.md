## Description:

Post or schedule content to Telegram channels and groups using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to draft API calls and configuration guidance for publishing or scheduling Telegram channel and group posts through Publora.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing through this workflow sends post text, scheduling details, and selected media to Publora.

Mitigation: Review content and media before submission, and only use Publora for data approved for that service.

Risk: The workflow requires a Publora API key and a Telegram bot with permission to post in the target channel or group.

Mitigation: Store the API key securely and grant the Telegram bot only the permissions needed for the intended destination.

Risk: Telegram Bot API limits can cause failed posts when media, captions, or message text exceed platform limits.

Mitigation: Keep media under documented Bot API limits, reduce captions to 1,024 characters for media posts, and move longer text to a text-only message body.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sergebulaev/skills/publora-telegram)
- [Publora API Base URL](https://api.publora.com/api/v1)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown with JavaScript and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, scheduling fields, Telegram platform identifiers, media upload steps, and limit guidance.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
