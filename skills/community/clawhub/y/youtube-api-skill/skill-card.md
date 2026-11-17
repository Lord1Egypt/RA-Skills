## Description:

Helps agents search YouTube, inspect channels and videos, and manage playlists, subscriptions, and comments through a user's connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use this skill to research YouTube content and manage their connected account's playlists, subscriptions, and comments, with approval before account changes or automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected-account actions can change playlists, subscriptions, comments, or authorization.

Mitigation: Start with read/list requests and confirm the account and exact resource before approving writes or a new connection.

Risk: Approved hosted functions and triggers can create persistent automations using the connected account.

Mitigation: Require explicit approval of each automation, its permissions, and the actions it will perform.

Risk: Raw API-key mode exposes a long-lived credential to the calling environment.

Mitigation: Prefer OAuth through the CLI; use raw API-key mode only when the CLI cannot be used, and never log or persist the key.

## Reference(s):

- [ClawHub YouTube skill](https://clawhub.ai/byungkyu/skills/youtube-api-skill)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [YouTube Data API overview](https://developers.google.com/youtube/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Text or Markdown with CLI commands and structured API results where requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include account and channel data; write actions require user confirmation.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
