## Description:

Use this skill for XCrawl crawl tasks, including bulk site crawling, crawler rule design, async status polling, and delivery of crawl output for downstream scrape and search workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wykings](https://clawhub.ai/user/wykings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to plan bounded XCrawl crawl requests, submit them to XCrawl, poll asynchronous crawl status, and return raw crawl responses for downstream scrape, search, or extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unnecessary file-editing permissions for a crawling skill.

Mitigation: Review allowed tools before installation and prefer a version that limits runtime permissions to curl and node.

Risk: The security evidence reports an unsafe TLS default that could expose sensitive crawl credentials.

Mitigation: Use crawl requests that keep TLS verification enabled and avoid sending sensitive cookies or headers unless TLS verification is explicitly enabled.

Risk: Crawl URLs and request payloads are sent to XCrawl and may consume account credits.

Mitigation: Use bounded crawl scopes, exclude sensitive paths, and confirm account credit impact before running large crawls.

## Reference(s):

- [XCrawl homepage](https://www.xcrawl.com/)
- [XCrawl dashboard](https://dash.xcrawl.com/)
- [XCrawl Crawl API endpoint](https://run.xcrawl.com/v1/crawl)
- [ClawHub release page](https://clawhub.ai/wykings/skills/xcrawl-crawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with JSON request and response bodies plus Bash and Node examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw XCrawl create and result responses unless the user explicitly requests a summary.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
