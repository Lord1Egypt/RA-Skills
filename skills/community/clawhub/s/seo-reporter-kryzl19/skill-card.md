## Description:

Audits a webpage URL for core SEO factors and generates a scored markdown report with specific recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site operators use this skill to run quick single-page SEO checks and prioritize improvements to metadata, headings, indexing signals, social previews, mobile viewport, and HTTPS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit script can make unrestricted web requests from the agent environment and follows redirects.

Mitigation: Use it only for public websites you intend to audit, and avoid internal, private, or sensitive network addresses.

Risk: The report is a quick single-page SEO check, not a full technical crawl, page-speed audit, backlink analysis, or keyword research workflow.

Mitigation: Treat results as triage guidance and use dedicated SEO tooling for broader site audits or specialized analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kryzl19/skills/seo-reporter-kryzl19)

## Skill Output:

**Output Type(s):** [markdown, guidance, shell commands]

**Output Format:** [Markdown SEO audit report with score tables, findings, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; makes read-only HTTP requests to the target URL plus related robots.txt and sitemap.xml paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
