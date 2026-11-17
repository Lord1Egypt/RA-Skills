## Description:

Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa for research, monitoring, engagement, and approved publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research X/Twitter accounts, timelines, tweets, trends, and conversations, then prepare or publish posts only after explicit authorization. It supports monitoring and engagement workflows that require AISA_API_KEY-backed API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured AISA_API_KEY may appear in normal command output or shared transcripts.

Mitigation: Use a low-privilege, revocable key and avoid running status, authorize, or post commands in logs or shared transcripts until key echoing is fixed.

Risk: Posting and authorization requests can be redirected to arbitrary HTTP or HTTPS relay URLs.

Mitigation: Leave TWITTER_RELAY_BASE_URL unset or set it only to a trusted HTTPS relay endpoint.

Risk: The skill can publish posts or upload media to X/Twitter once authorized.

Mitigation: Require explicit user approval before publishing any post or media upload and verify the API response before claiming success.

## Reference(s):

- [Twitter OAuth posting reference](references/post_twitter.md)
- [AIsa API endpoint](https://api.aisa.one/apis/v1)
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/twitter-command-center-search-post)
- [Publisher profile](https://clawhub.ai/user/baofeng-tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authorization links, tweet identifiers, tweet links, search results, timeline summaries, or error messages from the relay/API.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
