## Description:

Guides configuration and auditing of robots.txt for search engine and AI crawler control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO practitioners use this skill to audit crawler access and produce robots.txt recommendations for search engines and AI crawlers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate on broad crawler-related requests where indexing, metadata, sitemap, or general crawlability guidance may be more appropriate.

Mitigation: Confirm the user is asking for robots.txt crawl control before applying recommendations, and redirect to the more specific indexing or crawlability topic when needed.

Risk: Incorrect robots.txt recommendations can accidentally block important site resources or pages from crawler access.

Mitigation: Review proposed disallow rules against the site's indexing goals and verify that assets required for rendering remain crawlable.

## Reference(s):

- [Vercel/MERJ AI crawler study](https://vercel.com/blog/the-rise-of-the-ai-crawler)
- [Google robots.txt documentation](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with robots.txt examples and compliance checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current-state audit notes, a recommended robots.txt file, and crawler-specific allow or disallow guidance.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
