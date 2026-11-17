## Description:

Bypass website blocks and scrape web content using Scrapeless Universal Scraping API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapelesshq](https://clawhub.ai/user/scrapelesshq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to retrieve web content through Scrapeless for web scraping, data pipelines, AI data collection, market intelligence, SEO monitoring, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party scraping service to bypass website protections.

Mitigation: Use it only for sites and data the user is authorized to access.

Risk: Requests can send headers, POST data, proxy URLs, and target content to Scrapeless.

Mitigation: Do not pass cookies, Authorization headers, private endpoints, regulated data, or credential-bearing proxy URLs without approval.

Risk: The skill installs and runs Python dependencies and network code.

Mitigation: Install in an isolated environment and pin or audit dependencies before use.

Risk: Per-request billing and rate limits may affect automated workflows.

Mitigation: Throttle request frequency, monitor 429 responses, and confirm billing expectations before high-volume use.

## Reference(s):

- [Scrapeless Homepage](https://www.scrapeless.com)
- [Scrapeless Universal Scraping API](https://docs.scrapeless.com/en/universal-scraping-api/)
- [Scrapeless Universal Scraping API Product Page](https://www.scrapeless.com/en/product/universal-scraping-api)
- [ClawHub Skill Page](https://clawhub.ai/scrapelesshq/skills/scrapeless-webunlocker-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON objects containing scraped content, extracted data, screenshots, network logs, or error details; documentation includes Markdown and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X_API_TOKEN. Supports HTML, plaintext, Markdown, PNG, JPEG, network, and structured content responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
