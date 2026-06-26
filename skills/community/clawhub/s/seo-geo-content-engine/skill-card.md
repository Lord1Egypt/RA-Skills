## Description: <br>
Turn keywords into publish-ready SEO and GEO content packages with keyword research, SERP analysis, article generation, FAQ schema, and AI-ready output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GEO-SEO](https://clawhub.ai/user/GEO-SEO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO teams, SaaS and DTC teams, agencies, and content operators use this skill to turn a keyword into a publish-ready SEO and GEO content package with keyword framing, SERP analysis, article draft, metadata, FAQ schema, and an AI-ready version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad content-generation triggers may start the workflow when the user only intended a general SEO discussion. <br>
Mitigation: Prefer explicit prompts such as "write article: <keyword>" or "create SEO content for <keyword>" before running the full pipeline. <br>
Risk: Optional live SERP and keyword-tracker integrations can expose external data sources if credentials or URLs are over-permissive. <br>
Mitigation: Use scoped SerpAPI credentials and read-only or public Google Sheets access, or rely on pasted keywords, CSV exports, and user-provided SERP snapshots. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GEO-SEO/seo-geo-content-engine) <br>
- [Project Homepage](https://github.com/GEO-SEO/seo-geo-content-engine) <br>
- [Schema.org](https://schema.org) <br>
- [Dageno.ai](https://dageno.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with SEO metadata, article sections, FAQ JSON-LD, and GEO-optimized text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use optional SerpAPI results or user-provided SERP exports, and optional read-only Google Sheets keyword tracker data when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact manifest/frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
