## Description:

Extract readable content from public web pages for articles, documentation, product pages, and URL text capture, while avoiding login-required, interactive, or JavaScript-heavy sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lesliepie](https://clawhub.ai/user/lesliepie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use WebScraper to fetch public web pages and convert article, documentation, or product-page content into readable markdown or text for summarization, lookup, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching internal, private, cloud-metadata, or secret-bearing URLs could expose sensitive information to the agent.

Mitigation: Restrict use to public URLs that are intended to be shared with the agent; block localhost, private network ranges, and cloud metadata endpoints.

Risk: Web scraping can violate site terms, robots.txt, rate limits, or copyright expectations.

Mitigation: Respect robots.txt and site terms, prefer official APIs when available, include attribution, and use delays between requests.

Risk: Optional global npm installation of parsing helpers can introduce unpinned supply-chain risk.

Mitigation: Avoid global installs where possible; pin dependencies and install them in an isolated project environment.

Risk: The skill is not suited to login-required, CAPTCHA-protected, interactive, or JavaScript-heavy pages.

Mitigation: Use a browser-based agent with an appropriate session for those pages, or decline when access would bypass authentication or anti-abuse controls.

## Reference(s):

- [WebScraper ClawHub Skill Page](https://clawhub.ai/lesliepie/skills/webscraper)
- [OpenClaw Web Tool Documentation](https://docs.openclaw.ai/tools/web)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown or plain text with optional shell command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fetched source URLs, extraction mode guidance, length limits, summaries, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
