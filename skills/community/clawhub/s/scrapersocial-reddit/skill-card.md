## Description:

Retrieves public Reddit posts, comments, subreddit details, user profiles, and search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to retrieve public Reddit discussions and profiles for topic research, community discovery, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the ScraperSocial API key are sent to ScraperSocial.

Mitigation: Use this skill only if that data transfer is acceptable; keep the API key private.

Risk: Paginated results consume credits per returned item.

Mitigation: Set deliberate result limits and use cursors only when additional pages are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/scrapersocial-reddit)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public, read-only Reddit data; paginated results can include a cursor, and responses include a request ID.]

## Skill Version(s):

1.0.4 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
