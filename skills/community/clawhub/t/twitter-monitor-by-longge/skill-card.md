## Description:

Monitor X/Twitter accounts for new tweets and send notifications to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmmuffin](https://clawhub.ai/user/mmmuffin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run a lightweight monitor for selected X/Twitter accounts and receive Telegram notifications when new tweets appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter session cookies can grant account access and are passed to xreach as process arguments.

Mitigation: Use a disposable or low-risk X/Twitter session where possible, avoid shared hosts, and rotate or revoke credentials after use.

Risk: The skill depends on an external xreach tool to fetch tweets.

Mitigation: Verify the source and version of xreach before installation and execution.

Risk: Telegram bot credentials and notification destinations control where tweet alerts are sent.

Mitigation: Use a dedicated Telegram bot token, confirm the chat ID before running, and limit access to the configured environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmmuffin/skills/twitter-monitor-by-longge)
- [Publisher profile](https://clawhub.ai/user/mmmuffin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands and environment variable guidance for Twitter and Telegram credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
