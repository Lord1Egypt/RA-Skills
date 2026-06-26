## Description: <br>
Audits crawlability, indexability, Core Web Vitals, mobile readiness, HTTPS/security, redirects, structured data, URL structure, and technical SEO evidence gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External site owners, SEO practitioners, and developers use this skill to diagnose technical SEO issues on sites they own or are authorized to test, then turn the findings into prioritized repair plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk sitemap or multi-URL audits can generate traffic against target sites. <br>
Mitigation: Use the skill only on sites the user owns or is authorized to test, sample representative URL groups where appropriate, and avoid unnecessary repeated fetches. <br>
Risk: Fetched web pages can contain prompt-injection text or misleading audit directives. <br>
Mitigation: Treat fetched page content as untrusted evidence, not instructions, and preserve the agent's existing instruction hierarchy. <br>
Risk: Audit notes, analytics data, or Search Console details may contain sensitive business information. <br>
Mitigation: Review summaries before saving them to memory or shared files, and retain only the evidence needed for follow-up work. <br>
Risk: Technical SEO recommendations may be incomplete when connector data, crawler output, or current search-console evidence is unavailable. <br>
Mitigation: Mark unsupported checks as unavailable, cite the evidence source and audit date, and validate production changes against trusted site data before rollout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/technical-seo-checker) <br>
- [Project Homepage](https://github.com/aaron-he-zhu/seo-geo-claude-skills) <br>
- [Robots.txt Reference Guide](references/robots-txt-reference.md) <br>
- [HTTP Status Codes for Technical SEO](references/http-status-codes.md) <br>
- [Technical SEO Checker - Compact Output Templates](references/technical-audit-templates.md) <br>
- [Technical SEO Checker Worked Example and Checklist](references/technical-audit-example.md) <br>
- [Technical SEO - Site-Wide / Bulk Audit Playbook](references/bulk-audit-playbook.md) <br>
- [E-commerce Platform SEO Patterns](references/ecommerce-platform-patterns.md) <br>
- [LLM Crawler Handling](references/llm-crawler-handling.md) <br>
- [Technical SEO - Pre-Migration Playbook](references/pre-migration-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown audit report with scorecards, evidence tables, prioritized fixes, and a handoff summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include robots.txt snippets, redirect maps, platform-specific checks, and memory-ready audit summaries when requested.] <br>

## Skill Version(s): <br>
9.9.9 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
