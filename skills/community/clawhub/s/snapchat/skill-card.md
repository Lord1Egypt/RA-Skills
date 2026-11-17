## Description:

Helps agents manage Snapchat advertising resources and review performance through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers and marketing teams use this skill to manage Snapchat ad accounts, campaigns, ads, creatives, and audiences, and to inspect campaign performance. It also guides user-approved automation through hosted functions and triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to advertising resources or connections can affect live accounts.

Mitigation: Start with read-only operations and obtain explicit user approval for every write or new connection.

Risk: Triggers, hosted functions, and destinations can run actions or forward events repeatedly.

Mitigation: Review each automation and destination before approval, scope event triggers narrowly, and grant separate approval for persistent forwarding.

Risk: Raw API keys and responses may expose credentials or personal data.

Mitigation: Prefer OAuth through the CLI, use raw API keys only when the CLI is unavailable, and disclose only task-relevant response fields.

## Reference(s):

- [ClawHub Snapchat skill](https://clawhub.ai/byungkyu/skills/snapchat)
- [Maton](https://maton.ai)
- [Snapchat Ads API introduction](https://developers.snap.com/api/marketing-api/Ads-API/introduction)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with commands and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ad performance summaries and proposed account changes.]

## Skill Version(s):

1.2.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
