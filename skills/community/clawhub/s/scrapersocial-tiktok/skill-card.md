## Description:

Retrieves public TikTok transcripts, summaries, engagement metrics, comments, audience profiles, songs, and search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to retrieve and analyze public TikTok videos, creators, comments, audiences, and trends through the ScraperSocial API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request shares the API key and requested TikTok identifiers or queries with ScraperSocial.

Mitigation: Use a dedicated API key and send only public-data requests that the user intended.

Risk: Broad follower or comment collection may incur substantial credit costs and data volume.

Mitigation: Confirm the scope before large collections; limit results and paginate selectively.

## Reference(s):

- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)
- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-tiktok)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON responses containing public TikTok data and API-generated summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include a request ID; paginated results may include a cursor.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
