## Description: <br>
Scrape a single page or crawl a full website using WebCrawlerAPI to return or save markdown content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n10ty](https://clawhub.ai/user/n10ty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to retrieve markdown from a specific URL or crawl a website into local markdown files. It is useful when an agent needs webpage content in a text format for review, summarization, or follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested URLs and crawled content to WebCrawlerAPI. <br>
Mitigation: Use it only for sites whose content may be shared with WebCrawlerAPI, and avoid private or internal sites unless that use is approved. <br>
Risk: The skill requires a WebCrawlerAPI API key. <br>
Mitigation: Store the key in WEBCRAWLERAPI_API_KEY, keep it out of source files and prompts, and prefer a revocable or scoped key when possible. <br>
Risk: Crawl mode stores markdown files locally. <br>
Mitigation: Review generated files under .webcrawlerapi/<hostname>/ before relying on them or sharing them. <br>
Risk: Broad web search or web fetch wording may trigger the skill outside the intended scrape or crawl use case. <br>
Mitigation: Confirm the target URL and whether the user wants a single-page scrape or a website crawl before running commands. <br>


## Reference(s): <br>
- [WebCrawlerAPI](https://webcrawlerapi.com/) <br>
- [WebCrawlerAPI dashboard access](https://dash.webcrawlerapi.com/access) <br>
- [ClawHub skill page](https://clawhub.ai/n10ty/webcrawler) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown returned in conversation for single-page scrape, or markdown files saved under .webcrawlerapi/<hostname>/ for crawls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Crawl mode defaults to 25 pages and reports crawl totals, success and failure counts, and saved file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
