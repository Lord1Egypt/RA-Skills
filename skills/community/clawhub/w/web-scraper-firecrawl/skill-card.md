## Description:

Web scraping and content extraction using Firecrawl API for crawling websites, extracting structured data, converting web pages to markdown, scraping multiple URLs, and building knowledge bases from web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape single pages, crawl sites, discover URLs, batch-process URL lists, and extract structured web data through Firecrawl. It is suited for knowledge-base building, research and analysis, and content migration workflows where sending target URLs and scraped content to Firecrawl is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, extraction prompts, schemas, and scraped page content are sent to the third-party Firecrawl API.

Mitigation: Use only approved public or non-confidential pages, and avoid internal, authenticated, regulated, or confidential content unless explicitly authorized.

Risk: The skill depends on FIRECRAWL_API_KEY for API access.

Mitigation: Keep the API key scoped, protected, and out of logs, prompts, source files, and shared outputs.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/antonia-sz/skills/web-scraper-firecrawl)
- [Firecrawl website](https://firecrawl.dev)
- [Firecrawl GitHub repository](https://github.com/mendableai/firecrawl)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, links, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; Firecrawl CLI results may be markdown, HTML, JSON, link lists, screenshots, or saved files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIRECRAWL_API_KEY and sends requested URLs, extraction prompts, schemas, and scraped content to Firecrawl.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
