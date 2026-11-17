## Description:

Pull Weibo user profiles and posts, post comments/likes/reposts, keyword search across posts, videos, users, topics and images, the hot-search board and ranking boards, and channel feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to retrieve structured Weibo user, post, search, trend, ranking, and channel data through Scavio API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send Weibo IDs, post IDs, and search terms to Scavio.

Mitigation: Use the skill only for data you are comfortable sharing with Scavio.

Risk: The Scavio API key can authorize paid or metered requests.

Mitigation: Keep SCAVIO_API_KEY out of source control and load it from a trusted secret store or environment variable.

Risk: Every API request may consume credits, including empty-result requests.

Mitigation: Validate required identifiers and pagination cursors before issuing requests.

## Reference(s):

- [Scavio Weibo API documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/weibo-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON API payloads, Python examples, and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses use structured JSON envelopes with data, response_time, credits_used, and credits_remaining.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
