## Description:

Retrieve public Hacker News stories, comment threads, user profiles, and keyword search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to retrieve public Hacker News discussions, profiles, and search results for analysis or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested results consume ScraperSocial API credits.

Mitigation: Limit result counts and check expected credit use before requesting large searches or comment threads.

Risk: Access requires sharing an API key with a third-party service.

Mitigation: Keep SCRAPERSOCIAL_KEY private and scoped, and use the service only if its terms and data handling are acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-hacker-news)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [JSON data, Text]

**Output Format:** [JSON responses for stories, comments, profiles, and search results; text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and comment results may be paginated; responses include a request ID.]

## Skill Version(s):

1.0.4 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
