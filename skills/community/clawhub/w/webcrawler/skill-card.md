## Description:

Scrape a single page or crawl a full website using WebCrawlerAPI and return or save the results as markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n10ty](https://clawhub.ai/user/n10ty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users use GetMarkdown to fetch public web page content as markdown or crawl public websites into local markdown files via WebCrawlerAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs are sent to WebCrawlerAPI and may disclose sensitive targets if users submit internal or authenticated pages.

Mitigation: Use the skill for public pages, avoid internal or authenticated URLs, and review each URL before requesting a scrape or crawl.

Risk: Full-site crawls can collect unintended pages and store crawl output in the working directory.

Mitigation: Review crawl scope before use, keep the default item limit unless broader coverage is needed, and inspect files saved under .webcrawlerapi/<hostname>/ before reuse.

Risk: The skill requires a WebCrawlerAPI API key.

Mitigation: Provide the key through WEBCRAWLERAPI_API_KEY and do not hardcode it in commands, files, or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n10ty/skills/webcrawler)
- [WebCrawlerAPI](https://webcrawlerapi.com/)
- [WebCrawlerAPI dashboard access](https://dash.webcrawlerapi.com/access)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses and local .md files, with Bash/curl commands for WebCrawlerAPI calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-page scrape returns markdown directly; full-site crawl saves .md files under .webcrawlerapi/<hostname>/ with a default 25-page limit.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
