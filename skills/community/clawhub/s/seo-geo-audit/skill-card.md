## Description:

Run a unified SEO and GEO audit for a website, page, or domain that combines technical findings, content quality, trust signals, and AI citation readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geo-seo](https://clawhub.ai/user/geo-seo)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO operators, founders, agencies, and growth teams use this skill to evaluate a public website or domain across technical SEO, content quality, trust, entity authority, off-site visibility, and AI search readiness. It produces a prioritized audit that separates observed evidence from assessment and marks unavailable private data as not verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may overstate certainty when private analytics, Search Console, server logs, backlink data, or AI citation monitoring are unavailable.

Mitigation: Separate observed evidence from assessment and mark missing inputs as Not verified.

Risk: Optional search enrichment can send target queries or public-site context to a third-party search provider.

Mitigation: Configure SERPAPI_API_KEY only when search-result enrichment is intended and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/geo-seo/skills/seo-geo-audit)
- [Scoring Framework](artifact/references/scoring-framework.md)
- [Operator Output Template](artifact/references/output-template.md)
- [Chinese Boss Output Template](artifact/references/output-template-zh-boss.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports boss, operator, and specialist report modes; missing private analytics, Search Console, crawl logs, backlink data, and AI citation monitoring are marked Not verified.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
