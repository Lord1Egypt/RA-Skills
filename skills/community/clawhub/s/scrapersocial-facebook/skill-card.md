## Description:

Retrieve public Facebook posts, page statistics, comments, ads, listings, events, video transcripts, and summaries through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to retrieve and analyze public Facebook content, page activity, advertising, and video transcripts without accessing private accounts or posting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facebook URLs, handles, and search terms are sent to ScraperSocial using a ScraperSocial API key.

Mitigation: Use only when sharing those inputs with ScraperSocial is acceptable; keep the API key private.

Risk: Requests consume API credits, especially transcripts, summaries, downloads, and paginated results.

Mitigation: Make calls only when needed and limit or page results deliberately.

## Reference(s):

- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)
- [ScraperSocial API guidance](https://scrapersocial.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured JSON data or natural-language answers based on retrieved public data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; some results are paginated and video download links expire.]

## Skill Version(s):

1.0.4 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
