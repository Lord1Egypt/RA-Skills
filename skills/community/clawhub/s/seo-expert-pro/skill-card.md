## Description: <br>
Enable SEO superpowers for OpenClaw with structured guidance for technical SEO, content SEO, site structure, and measurement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realm1lf](https://clawhub.ai/user/realm1lf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, SEO practitioners, developers, and site owners use this skill to guide SEO audits and implementation checks for crawling, indexing, metadata, structured data, site architecture, and search measurement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional curl use can send HTTP requests to user-provided sites. <br>
Mitigation: Allow curl only under the host policy you intend, and review target URLs before running diagnostics. <br>
Risk: Search Console, Analytics, or SEO API credentials could be exposed if entered into chat or committed to skill files. <br>
Mitigation: Store credentials only in gateway environment configuration and reference environment variable names in conversation. <br>
Risk: SEO recommendations can become stale as search platform guidance and algorithms change. <br>
Mitigation: Prefer current primary sources such as Google Search Central or Bing Webmaster documentation when limits, eligibility, or compliance matter. <br>
Risk: SEO guidance can be misused to imply guaranteed rankings or unsupported outcomes. <br>
Mitigation: Use the skill for discoverability, quality, and measurement hygiene, and avoid promises of rankings or instant results. <br>


## Reference(s): <br>
- [Google Search Central Documentation](https://developers.google.com/search/docs) <br>
- [ClawHub listing: SEO Expert](https://clawhub.ai/realm1lf/seo-expert-pro) <br>
- [Publisher profile: realm1lf](https://clawhub.ai/user/realm1lf) <br>
- [SEO Expert reference index](references/OVERVIEW.md) <br>
- [Authentication and secrets guidance](references/AUTH.md) <br>
- [SEO fundamentals](references/01_seo_grundlagen.md) <br>
- [Crawling and indexing](references/02_crawling_indexierung.md) <br>
- [Monitoring and troubleshooting](references/04_monitoring_fehlerbehebung.md) <br>
- [Ranking and search appearance hub](references/03_ranking_darstellung.md) <br>
- [Web-specific SEO guides hub](references/05_webspezifische_leitfaeden.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, recommendations, inline shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include user-directed HTTP diagnostics when curl is available and allowed by host policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; bundled skill metadata version 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
