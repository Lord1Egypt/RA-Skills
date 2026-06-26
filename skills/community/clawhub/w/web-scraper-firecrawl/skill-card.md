## Description: <br>
Web scraping and content extraction using Firecrawl API for crawling sites, extracting structured data, converting web pages to markdown, processing multiple URLs, and building knowledge bases from web content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scrape, crawl, map, batch process, and extract structured data from web pages through Firecrawl. It is useful for preparing markdown, JSON, HTML, link lists, screenshots, and local exports for research, migration, analysis, or knowledge-base workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, page content, schemas, prompts, and extracted data may be sent to the external Firecrawl service. <br>
Mitigation: Use a dedicated, revocable Firecrawl API key and avoid private URLs, internal systems, secrets, or confidential data in scrape targets and schemas. <br>
Risk: Scraping unauthorized or restricted content can violate site terms, policy, or law. <br>
Mitigation: Scrape only content the user is authorized to process and review target-site requirements before crawling or batch scraping. <br>
Risk: Exported crawl or extraction results may persist sensitive or unwanted content locally. <br>
Mitigation: Write outputs only to reviewable locations and clean up exported files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/antonia-sz/web-scraper-firecrawl) <br>
- [Firecrawl service](https://firecrawl.dev) <br>
- [Firecrawl project](https://github.com/mendableai/firecrawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, markdown, HTML, JSON, link lists, screenshots, and saved local files depending on the Firecrawl command and requested formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FIRECRAWL_API_KEY and can write scraped or extracted results to user-specified output files or directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
