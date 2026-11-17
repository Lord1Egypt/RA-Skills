## Description:

Helps agents retrieve YouTube channel analytics reports and manage video, playlist, and channel groups through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, analysts, and developers use this skill to review channel performance by date, country, or video and to manage analytics groups for connected YouTube accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account exposes its authorized YouTube Analytics data to the integration.

Mitigation: Confirm account connections with the user, choose only needed OAuth scopes, and use the pinned CLI.

Risk: Group changes or hosted automations can modify analytics organization or run without further prompts.

Mitigation: Obtain separate approval for each write, hosted function, and trigger before enabling it.

Risk: Trigger destinations can continuously forward connected-account or event data to third parties.

Mitigation: Confirm the exact destination and data shared; avoid third-party forwarding unless the user explicitly trusts it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/youtube-analytics-api)
- [Maton](https://maton.ai)
- [YouTube Analytics API documentation](https://developers.google.com/youtube/analytics)
- [YouTube Analytics API reference](https://developers.google.com/youtube/analytics/reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with analytics summaries, API examples, and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include channel metrics and group details available to the authorized connection.]

## Skill Version(s):

1.2.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
