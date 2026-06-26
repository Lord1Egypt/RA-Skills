## Description: <br>
XCrawl Scraper helps agents use the XCrawl API to scrape web pages, search the web, map sites, crawl sites, and extract structured data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangss110](https://clawhub.ai/user/zhangss110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure XCrawl credentials, run scraping and crawling commands, and collect page content or structured JSON from target sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the XCrawl API key in a local plaintext config file. <br>
Mitigation: Use a dedicated API key, keep scripts/config.json out of shared folders and source control, and rotate the key if it is exposed. <br>
Risk: The skill can scrape, crawl, or search content that may be private, regulated, or unauthorized. <br>
Mitigation: Use it only on content you are authorized to access and avoid private or regulated data unless the workflow has appropriate approval. <br>
Risk: The skill depends on the third-party XCrawl service and xcrawl Python package. <br>
Mitigation: Install and run it only when you trust XCrawl, the package source, and the service endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangss110/xcrawl-scraper) <br>
- [XCrawl website](https://xcrawl.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, screenshots, shell commands, configuration] <br>
**Output Format:** [CLI output, Markdown, HTML, JSON, and screenshot URLs or data returned by XCrawl] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, pip, the xcrawl package, and an XCrawl API key stored in scripts/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
