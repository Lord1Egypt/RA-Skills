## Description:

X (Twitter) data toolkit via ScraperSocial for public profiles, posts, lists, search, video transcripts, summaries, and post statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to look up public X/Twitter posts and profiles, search posts, monitor lists, and obtain video transcripts or summaries through ScraperSocial.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key and requested searches, handles, and post URLs are sent to ScraperSocial.

Mitigation: Confirm third-party service use is appropriate, protect the API key, and submit only suitable public-data queries.

Risk: Queries, transcripts, and summaries can consume account credits.

Mitigation: Check credit costs before calling endpoints and avoid speculative transcript or summary requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-twitter)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public X/Twitter data; responses include a request ID and paginated results may include a cursor.]

## Skill Version(s):

1.0.4 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
