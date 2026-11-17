## Description:

Use ScrapeBadger APIs to retrieve web search, marketplace, social, real-estate, and AI answer data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xghostcasper](https://clawhub.ai/user/0xghostcasper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use ScrapeBadger to retrieve public search, marketplace, social, real-estate, and AI answer data through documented APIs for research, comparison, and application workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis had medium confidence and could not resolve four local path-like references; the skill also documents use of an API key.

Mitigation: Review the unresolved references before use and keep SCRAPEBADGER_API_KEY private in the environment rather than exposing it in prompts or logs.

## Reference(s):

- [ScrapeBadger API documentation](https://docs.scrapebadger.com)
- [Brave Search API overview](https://docs.scrapebadger.com/brave/overview)
- [GitHub profile API documentation](https://docs.scrapebadger.com/github/profiles)
- [GitHub repository API documentation](https://docs.scrapebadger.com/github/repositories)
- [ScrapeBadger MCP server](https://mcp.scrapebadger.com/mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured API response data, usually JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by API and query; market, pagination, and endpoint coverage limits apply.]

## Skill Version(s):

1.11.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
