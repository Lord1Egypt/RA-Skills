## Description:

Knowledge base for the 22 ScraperAPI MCP tools, covering scraping, Google, Amazon, Walmart, eBay, Redfin, and crawler workflows with tool selection, parameter optimization, credit cost guidance, and error recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scraperapitech](https://clawhub.ai/user/scraperapitech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to choose and configure ScraperAPI MCP tools for web scraping, search, shopping, real estate, crawler, SERP monitoring, SEO tracking, competitive intelligence, and market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes scraping, search, crawler, and structured extraction tasks through an external ScraperAPI service that requires an API key.

Mitigation: Install only when ScraperAPI routing is intended, store the key in environment variables, avoid exposing it in logs, prefer pinned and reviewed MCP helper versions, and rotate the key if exposure is suspected.

Risk: Broad crawl patterns, missing crawl budgets, or recurring schedules can consume credits quickly and collect more data than intended.

Mitigation: Use narrow URL include and exclude patterns, set crawlBudget and maxDepth, test with low depth first, and monitor or cancel jobs when scope or cost drifts.

Risk: Crawler callback URLs send scraped page results over the network and may expose sensitive, proprietary, or personal data.

Mitigation: Use callback URLs only with explicit approval, only send results to controlled HTTPS endpoints, and confirm the endpoint owner and data handling expectations before enabling callbacks.

Risk: Premium, ultraPremium, rendering, and geo-targeting options increase cost and may be unnecessary for simple pages.

Mitigation: Start with the standard scrape call, escalate only when content is missing or blocked, and do not combine mutually exclusive premium and ultraPremium settings.

## Reference(s):

- [ScraperAPI homepage](https://www.scraperapi.com)
- [ScraperAPI dashboard](https://www.scraperapi.com/dashboard)
- [ClawHub skill page](https://clawhub.ai/scraperapitech/skills/scraperapi-mcp)
- [MCP Server Setup](references/setup.md)
- [Scrape Tool](references/scraping.md)
- [Google Search Tools](references/google.md)
- [Amazon SDE Tools](references/amazon.md)
- [Walmart SDE Tools](references/walmart.md)
- [eBay SDE Tools](references/ebay.md)
- [Redfin SDE Tools](references/redfin.md)
- [Crawler Tools](references/crawler.md)
- [SERP and News Monitoring](recipes/serp-news-monitor.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured JSON outputs for SERP and news monitoring workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
