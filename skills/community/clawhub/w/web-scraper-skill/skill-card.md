## Description:

This skill helps agents scrape, crawl, map, search, and extract website data using Apify and Firecrawl APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to choose between Apify and Firecrawl, prepare authenticated API requests, run web scraping workflows, and handle extracted web data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping targets, queries, actor inputs, and results may be sent to Firecrawl or Apify.

Mitigation: Use the skill only when users understand this data sharing, and avoid confidential, internal, or authenticated pages without approval.

Risk: API tokens can be exposed when placed in query strings or hardcoded examples.

Mitigation: Prefer authorization headers and environment variables for tokens, and avoid query-string tokens.

Risk: Large or non-compliant scraping jobs may create legal, operational, or site-policy issues.

Mitigation: Start with small limits, check rate limits, and use site-compliant scraping practices.

## Reference(s):

- [Code Templates: Apify & Firecrawl](references/code-templates.md)
- [Firecrawl API Base URL](https://api.firecrawl.dev/v2)
- [Apify API Base URL](https://api.apify.com/v2)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with HTTP, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request patterns, authentication guidance, actor selection advice, polling workflows, and result handling examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
