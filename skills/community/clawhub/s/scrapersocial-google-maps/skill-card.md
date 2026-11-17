## Description:

Retrieves place details, search results, photos, and business contacts from public Google Maps data through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can research locations, find places by query, and retrieve business contact details or photos for local directories and lead lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and Google Maps URLs are sent to ScraperSocial, and requests may consume account credits.

Mitigation: Share only intended queries or URLs, review the provider's data handling, and set result limits before running requests.

Risk: Business contact results may be subject to local privacy and outreach rules.

Mitigation: Use contact data only where applicable privacy and outreach rules permit.

## Reference(s):

- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)
- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-google-maps)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON endpoint results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include a request ID; paginated responses may include a next cursor.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
