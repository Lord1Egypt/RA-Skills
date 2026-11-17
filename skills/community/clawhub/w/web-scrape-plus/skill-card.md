## Description:

Enhanced web scraping with anti-detection, proxy support, rate limiting, data validation, and multiple extraction methods for static pages, dynamic content, login-gated sites, and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan authorized web data extraction workflows and generate scraping guidance, examples, and configuration patterns for static pages, dynamic content, API endpoints, login-gated sites, and paginated sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated scraping and session-cookie handling can expose accounts or sensitive session material.

Mitigation: Use test accounts where possible, avoid sharing or storing raw session cookies, and limit access to credentials and session artifacts.

Risk: Proxy rotation, anti-detection techniques, or scraping at scale can violate site policies or legal expectations.

Mitigation: Use the skill only for sites where scraping is authorized, check applicable policies before use, and avoid stealth or proxy behavior unless explicitly permitted.

Risk: Poorly bounded scraping can overload target services or collect data beyond the intended scope.

Mitigation: Apply rate limits, respect robots.txt and server limits, cache responses where appropriate, and validate that collected data matches the intended schema.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/web-scrape-plus)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with Python, JSON, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scraping workflows, implementation snippets, and output format examples; it does not execute scraping by itself.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
