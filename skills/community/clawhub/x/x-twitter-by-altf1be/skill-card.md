## Description:

Post tweets, threads, and media to X/Twitter via API v2 with OAuth 1.0a signing and minimal runtime dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to let an agent verify an X/Twitter API connection and publish tweets, replies, threads, or media posts from a configured account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live tweets, replies, threads, and media from the configured X/Twitter account.

Mitigation: Require the agent to preview the exact post content and receive explicit user approval before running any publish command.

Risk: The skill requires OAuth credentials with authority to post from the user's account.

Mitigation: Store credentials only in the configured environment, limit access to trusted agents, and rotate credentials if they may have been exposed.

## Reference(s):

- [X Developer Platform](https://developer.x.com)
- [ClawHub skill page](https://clawhub.ai/abdelkrim/skills/x-twitter-by-altf1be)
- [Publisher profile](https://clawhub.ai/user/abdelkrim)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger live X/Twitter API publish actions when the user provides credentials and approves execution.]

## Skill Version(s):

1.1.3 (source: server evidence, package.json, CLI version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
