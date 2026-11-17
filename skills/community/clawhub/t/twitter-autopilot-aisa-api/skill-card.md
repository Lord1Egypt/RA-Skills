## Description:

Twitter Autopilot helps agents read and search X (Twitter) data and, after user OAuth authorization, publish posts or perform likes, follows, and related account interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for Twitter/X research, social listening, trend and account monitoring, and OAuth-authorized publishing or engagement workflows without sharing account passwords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured AIsa API key can be exposed in normal outputs.

Mitigation: Review before installing; use a dedicated low-privilege, rotatable API key and avoid running status, authorize, or post with a real key unless secret redaction is fixed.

Risk: A configurable relay can receive the API key and user content.

Mitigation: Keep the default relay configuration; do not set TWITTER_RELAY_BASE_URL to a non-default or HTTP endpoint.

Risk: Posting, likes, follows, unfollows, and OAuth authorization can change a public X/Twitter account.

Mitigation: Require explicit user approval for each account-changing action and verify action success from the relay before claiming completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/twitter-autopilot-aisa-api)
- [Twitter Engagement Workflow](references/engage_twitter.md)
- [Twitter OAuth Workflow](references/post_twitter.md)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://aisa.one/docs/api-reference/)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown responses with shell or Python command invocations and API result summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; OAuth authorization is required before posting, likes, follows, or unfollows.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
