## Description: <br>
Knowledge base for the 22 ScraperAPI MCP tools, covering scraping, Google, Amazon, Walmart, eBay, Redfin, and crawler workflows with tool selection, parameter guidance, credit cost guidance, and error recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scraperapitech](https://clawhub.ai/user/scraperapitech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose and configure ScraperAPI MCP tools for web scraping, search, e-commerce research, real estate lookups, crawling, SERP monitoring, and recovery from scraping errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ScraperAPI requests send target URLs, searches, and scraped content through an external service. <br>
Mitigation: Use the skill only for authorized scraping and avoid collecting sensitive personal data unless permitted. <br>
Risk: The skill requires storing a ScraperAPI API key for MCP use. <br>
Mitigation: Store the key in the documented environment variable and avoid exposing it in prompts, logs, or generated artifacts. <br>
Risk: Crawler callback URLs can receive scraped page results and may expose sensitive or proprietary content. <br>
Mitigation: Approve callback URLs or recurring schedules only after confirming endpoint ownership, HTTPS use, destination, scope, and expected volume. <br>
Risk: Broad crawls, premium modes, rendering, and recurring schedules can increase cost and data volume. <br>
Mitigation: Keep crawl patterns and budgets narrow, start with the cheapest fetch strategy, and escalate only when required. <br>


## Reference(s): <br>
- [ScraperAPI](https://www.scraperapi.com) <br>
- [MCP Server Setup](references/setup.md) <br>
- [Scrape Tool Guide](references/scraping.md) <br>
- [Google Search Tools Guide](references/google.md) <br>
- [Amazon SDE Tools Guide](references/amazon.md) <br>
- [Walmart SDE Tools Guide](references/walmart.md) <br>
- [eBay SDE Tools Guide](references/ebay.md) <br>
- [Redfin SDE Tools Guide](references/redfin.md) <br>
- [Crawler Tools Guide](references/crawler.md) <br>
- [SERP & News Monitoring Recipe](recipes/serp-news-monitor.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/scraperapitech/scraperapi-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON examples, command snippets, and structured output recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or request scraped web content, search results, crawler job settings, and SERP/news monitoring JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
