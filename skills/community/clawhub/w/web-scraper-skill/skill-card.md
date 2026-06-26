## Description: <br>
Use this skill to scrape, crawl, or extract data from websites using Apify or Firecrawl APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishekj9621](https://clawhub.ai/user/abhishekj9621) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose between Apify and Firecrawl, prepare API calls, and extract page, crawl, search, social, map, ecommerce, or other web data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may use the skill for broad scraping, crawling, batch scraping, or third-party actor runs without sufficient user authorization. <br>
Mitigation: Require explicit confirmation before crawl, batch scrape, social, ecommerce, map, or other third-party actor runs, and use the skill only on sites the user is authorized to scrape. <br>
Risk: Scraping requests can transfer target URLs, page data, and user-provided inputs to Firecrawl or Apify. <br>
Mitigation: Avoid private, internal, or authenticated pages unless approved, and inform users when data will be sent to third-party scraping services. <br>
Risk: Example API tokens could be copied into code or shared in prompts. <br>
Mitigation: Store API tokens outside examples, prefer environment variables or approved secret storage, and avoid hardcoding credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhishekj9621/web-scraper-skill) <br>
- [Code templates](references/code-templates.md) <br>
- [Firecrawl API](https://api.firecrawl.dev/v2) <br>
- [Apify API](https://api.apify.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown with HTTP, JSON, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scraping plans, API request examples, polling workflows, and result-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
