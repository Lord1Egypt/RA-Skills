## Description:

XCrawl Scraper helps agents use the XCrawl web scraping API to scrape pages, search the web, map sites, crawl sites, and extract structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangss110](https://clawhub.ai/user/zhangss110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure XCrawl API access and run scraping, search, site mapping, crawling, and JSON extraction workflows from command-line tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested URLs and extracted content to the XCrawl service.

Mitigation: Use it only with URLs and content that are approved for processing by XCrawl, and avoid sensitive internal or regulated data unless that use is authorized.

Risk: The skill stores the XCrawl API key in a local configuration file and may display a partial key in configuration output.

Mitigation: Prefer a protected secret mechanism or tightly permissioned config file for API keys, and review local file access before installation.

Risk: The skill depends on the external xcrawl Python package and remote XCrawl API behavior.

Mitigation: Pin and review the xcrawl dependency in an isolated environment before using the skill for important work.

## Reference(s):

- [XCrawl Scraper on ClawHub](https://clawhub.ai/zhangss110/skills/xcrawl-scraper)
- [XCrawl Website](https://xcrawl.com)
- [XCrawl API Endpoint](https://run.xcrawl.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, screenshots, terminal text, and configuration JSON depending on the selected command and XCrawl output format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, pip, the xcrawl package, network access to XCrawl, and a configured XCrawl API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
