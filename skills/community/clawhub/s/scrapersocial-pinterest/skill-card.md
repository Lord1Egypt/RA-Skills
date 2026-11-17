## Description:

Retrieves public Pinterest pin details, keyword search results, and URL save counts through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to research public Pinterest pins and visual trends or check how often a URL has been saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs or search terms and the API key are sent to ScraperSocial.

Mitigation: Use a key with only the access needed and avoid submitting sensitive URLs or searches.

Risk: Successful requests consume ScraperSocial credits, including per-pin search charges.

Mitigation: Check the request and result limit before running a search or paging through results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-pinterest)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [JSON responses, Shell commands, Guidance]

**Output Format:** [JSON for pin details, search results, and URL save counts; text guidance for invoking the scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated results may include a next cursor; responses include a request ID.]

## Skill Version(s):

1.0.4 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
