## Description:

Retrieves public Google Play app details, reviews, keyword search results, and categories through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app marketers use this skill to inspect public Android app listings, monitor reviews, and research Google Play search results and categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill grants access to a ScraperSocial API key.

Mitigation: Provide the key only to trusted executions and keep it out of shared output.

Risk: Requests spend ScraperSocial credits, including credits for returned reviews and search results.

Mitigation: Check expected costs and limit result counts before making requests.

Risk: Public storefront data does not include private Google Play Console metrics.

Mitigation: Use Play Console for installs, revenue, and other developer-account data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-google-play)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial API specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public storefront data; paginated responses may include a cursor and request ID.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
