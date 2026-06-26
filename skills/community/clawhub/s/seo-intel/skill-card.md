## Description: <br>
Local SEO competitive intelligence tool for SEO analysis, competitor research, keyword gaps, content strategy, site audits, AI citability, crawling, extraction, dashboards, and competitive action planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ukkometa](https://clawhub.ai/user/ukkometa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO operators, docs writers, and site owners use SEO Intel to crawl target and competitor sites, extract SEO and semantic signals, identify gaps, and turn findings into reports, briefs, action lists, or implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may crawl websites, store results locally, and use cloud models for analysis. <br>
Mitigation: Confirm crawl scope, avoid private or regulated content unless cloud processing is acceptable, and review generated reports before using them for decisions. <br>
Risk: The skill can guide agents toward editing and deploying live websites. <br>
Mitigation: Require a reviewed diff, confirm the exact site and Cloudflare project, and do not allow Wrangler deployment to run automatically. <br>
Risk: SEO recommendations and competitive analysis may be incomplete or misleading if crawl data, extraction, or model outputs are stale or wrong. <br>
Mitigation: Refresh the crawl and extraction pipeline before important use, inspect source evidence for high-impact changes, and treat generated action lists as proposals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ukkometa/seo-intel) <br>
- [Publisher profile](https://clawhub.ai/user/ukkometa) <br>
- [SEO Intel product page](https://ukkometa.fi/en/seo-intel/) <br>
- [Agent integration guide](AGENT_GUIDE.md) <br>
- [Database schema reference](references/db-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, code, shell commands, configuration] <br>
**Output Format:** [Markdown and structured JSON with inline shell commands, code snippets, reports, dashboards, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local reports, exports, SQLite-backed analysis results, website-change guidance, and deployment-oriented action plans.] <br>

## Skill Version(s): <br>
1.5.21 (source: server release metadata and skill heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
