## Description: <br>
Web scraping and data extraction using the Python Scrapling library, with support for static HTML pages, JavaScript-rendered pages, anti-bot or Cloudflare-protected sites, resilient selectors, session-based scraping, and JSON or Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PiyushZinc](https://clawhub.ai/user/PiyushZinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scrape websites, extract structured text, links, tables, prices, and similar page data, and build reusable scraping scripts with CSS or XPath selectors. It is intended for authorized scraping workflows that may need static fetching, JavaScript rendering, stealth browser behavior, or persisted session state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web scraping can involve protected sites, private pages, credentials, cookies, and saved page data. <br>
Mitigation: Install dependencies in an isolated environment, scrape only sites the user is authorized to access, avoid real credentials unless necessary, and clear saved sessions or DOM snapshots when handling private pages. <br>
Risk: Selectors can return empty or stale data when page structure changes. <br>
Mitigation: Use explicit error handling, log selector misses, validate required fields, and test at least one happy path and one edge case page before relying on extracted data. <br>


## Reference(s): <br>
- [Scrapling Reference](references/scrapling-reference.md) <br>
- [Reusable Scrapling extraction helper](scripts/extract_with_scrapling.py) <br>
- [ClawHub release page](https://clawhub.ai/PiyushZinc/scrapling-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with bash and Python examples; generated extraction results are JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use network requests, browser-based fetchers, local HTML parsing, selectors, timeouts, retries, session cookies, and saved DOM snapshots depending on the chosen extraction pattern.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
