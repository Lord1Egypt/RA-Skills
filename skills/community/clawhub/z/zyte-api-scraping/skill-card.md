## Description:

Extract structured data from websites using Zyte API with smart proxy rotation, browser rendering, service health checks, and account usage review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect OpenClaw to Zyte API through ClawLink, discover available Zyte tools, and run targeted website extraction, scraping, status, incident, maintenance, account, and usage workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping requests are routed through ClawLink and Zyte API using connected account credentials, which can expose URLs to external services.

Mitigation: Use only approved URLs, avoid confidential or internal targets unless organization policy allows it, and review the ClawLink and Zyte account trust boundary before use.

Risk: Large or repeated extraction jobs can affect Zyte API quotas, billing, and site-access limits.

Mitigation: Prefer targeted extraction, preview high-volume or batch work, confirm cost-sensitive operations, and monitor account usage.

Risk: Scraping may violate site rules or fail when sites block automated access.

Mitigation: Respect robots.txt and website terms of service, avoid unauthorized extraction, and check Zyte API status or adjust extraction settings when requests fail.

## Reference(s):

- [Zyte API Documentation](https://docs.zyte.com/zyte-api/)
- [Zyte API Overview](https://www.zyte.com/zyte-api/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zyte-api-scraping)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/zyte)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return extraction, status, usage, account, incident, and maintenance results from the connected Zyte API account.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
