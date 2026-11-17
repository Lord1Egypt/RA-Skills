## Description:

Use this skill for XCrawl search tasks, including keyword search request design, location and language controls, result analysis, and follow-up crawl or scrape planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wykings](https://clawhub.ai/user/wykings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to design and execute XCrawl keyword searches with explicit location, language, and result-limit controls. It returns the endpoint, request payload, raw response body, or request error details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, location or language settings, and API-key-bearing requests are sent to XCrawl.

Mitigation: Avoid submitting secrets, confidential business data, or sensitive personal information as search queries or request parameters.

Risk: The skill returns raw upstream response bodies, which may include incomplete, irrelevant, or untrusted web search results.

Mitigation: Review raw results before relying on them, and request a separate summary or analysis only when synthesis is needed.

Risk: Using XCrawl APIs consumes account credits.

Mitigation: Confirm account setup and available credits before running searches with high result limits or repeated requests.

## Reference(s):

- [XCrawl Homepage](https://www.xcrawl.com/)
- [XCrawl Dashboard](https://dash.xcrawl.com/)
- [XCrawl Search API Endpoint](https://run.xcrawl.com/v1/search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and raw XCrawl response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw upstream responses by default; summaries are only produced when explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
