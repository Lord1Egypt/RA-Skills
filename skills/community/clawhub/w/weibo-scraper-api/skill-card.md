## Description:

Pull Weibo user profiles and posts, post comments/likes/reposts, keyword search across posts, videos, users, topics and images, and the hot-search and ranking boards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, market researchers, and social-listening analysts use this skill to call Scavio's Weibo API for user, post, search, ranking, and hot-search data in structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weibo identifiers, post IDs, search terms, and request metadata are sent to Scavio and may reveal sensitive research interests.

Mitigation: Avoid submitting confidential topics, secrets, regulated personal data, or sensitive investigative targets unless sharing them with Scavio is acceptable.

Risk: API calls may consume paid credits, including calls that return empty results.

Mitigation: Check request parameters before calling endpoints, paginate deliberately, and monitor remaining credits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/weibo-scraper-api)
- [Scavio documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=weibo-scraper-api)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with JSON request examples, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API responses are structured JSON and Weibo endpoints cost credits.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
