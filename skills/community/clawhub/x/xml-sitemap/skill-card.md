## Description:

Helps agents create, audit, and optimize sitemap.xml files for search engine URL discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site maintainers, and SEO practitioners use this skill to generate or review XML sitemaps, sitemap indexes, robots.txt declarations, and related URL-discovery guidance for websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect sitemap guidance or generated examples could publish missing, non-canonical, or unintended URLs.

Mitigation: Review generated sitemap entries against the project's canonical URL source before publishing.

Risk: Large sites can exceed single-sitemap limits if URL counts are not checked.

Mitigation: Use a sitemap index and split sub-sitemaps when the site approaches or exceeds 50,000 URLs or 50MB uncompressed.

Risk: Inaccurate lastmod values can reduce trust in the sitemap.

Mitigation: Use page metadata or content modification timestamps, and omit lastmod where reliable modification data is unavailable.

Risk: Multilingual sitemap output can be wrong if locale alternates are guessed.

Mitigation: Derive locale URLs and hreflang alternates from project configuration and verify every language version self-references and cross-references the others.

## Reference(s):

- [sitemaps.org Protocol](https://www.sitemaps.org/protocol.html)
- [Google Search Central: Build and Submit a Sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with XML, TypeScript, configuration, and robots.txt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed for site-specific URL coverage, canonical host correctness, and accurate lastmod values before publishing.]

## Skill Version(s):

1.0.1 (source: evidence metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
