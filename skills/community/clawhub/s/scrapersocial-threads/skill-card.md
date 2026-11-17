## Description:

Retrieves public Threads profiles, posts, post engagement, keyword matches, and user search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to look up public Threads accounts, monitor posts and search terms, and review post engagement without publishing content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests send the ScraperSocial key and requested Threads handles, URLs, or search terms to ScraperSocial.

Mitigation: Confirm that sharing the credential and query data with this independent provider is acceptable before use.

Risk: Requests may consume ScraperSocial credits.

Mitigation: Check credit costs and limit or page results to control usage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-threads)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; paginated results can include a next cursor. Reply trees and view counts are unavailable.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
