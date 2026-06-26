## Description: <br>
Run a unified SEO and GEO audit for a website, page, or domain that combines technical findings, content quality, trust signals, and AI citation readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GEO-SEO](https://clawhub.ai/user/GEO-SEO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, founders, agencies, SEO operators, and AI-search growth teams use this skill to turn public website evidence into a prioritized SEO and GEO audit. It supports homepage, site, and domain visibility reviews with executive, operator, or specialist reporting modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Findings can be incomplete when the user has not provided private analytics, Search Console, server logs, or proprietary crawl data. <br>
Mitigation: Clearly separate observed public evidence from unverified inputs and mark unavailable data as Not verified. <br>
Risk: Search enrichment may send queries or target context to a third-party search-results provider when SERPAPI_API_KEY is configured. <br>
Mitigation: Only provide SERPAPI_API_KEY when third-party enrichment is intended; otherwise run from direct page and site observations. <br>
Risk: Broad crawl scopes can overreach the intended review area or consume unnecessary runtime. <br>
Mitigation: Set a clear target URL or domain and a reasonable crawl cap before running the audit. <br>


## Reference(s): <br>
- [Scoring Framework](references/scoring-framework.md) <br>
- [Operator and Specialist Output Template](references/output-template.md) <br>
- [Chinese Executive Output Template](references/output-template-zh-boss.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/GEO-SEO/seo-geo-audit) <br>
- [Dageno.ai](https://dageno.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with an executive summary, observed findings, assessments, priorities, and validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports boss, operator, and specialist report modes; marks unavailable private inputs as Not verified.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
