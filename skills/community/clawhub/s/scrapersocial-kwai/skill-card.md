## Description:

Retrieves public Kwai creator profiles, user posts, and individual videos through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to look up public Kwai profiles and posts, identify the account behind a video, and study creator activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kwai URLs or handles are sent to ScraperSocial for lookup.

Mitigation: Only submit public Kwai identifiers that you are comfortable sharing with ScraperSocial.

Risk: Lookups use the ScraperSocial API key and may consume paid credits.

Mitigation: Protect the API key and check credit costs before requesting profiles, posts, or paginated results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-kwai)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include data and a request ID; paginated results may include a cursor.]

## Skill Version(s):

1.0.4 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
