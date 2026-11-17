## Description:

Technical SEO Checker audits crawlability, indexing, Core Web Vitals, robots.txt, sitemaps, canonicals, redirects, migrations, and related technical SEO health signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, marketers, developers, and site operators use this skill to audit technical SEO health for a URL or domain. It produces scored findings and a prioritized repair plan for crawlability, indexability, site speed, mobile behavior, HTTPS, URL structure, structured data, international SEO, migrations, and bulk site audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audits may send private URLs, page contents, or business-sensitive SEO data to third-party SEO, rendering, validation, or crawler services.

Mitigation: Require explicit approval before using external services for private, staging, authenticated, or tokenized URLs; prefer local tools where possible.

Risk: URLs may contain sensitive query parameters or access tokens that could be exposed during validation or crawling.

Mitigation: Strip sensitive query parameters and tokens before fetching, rendering, or validating URLs.

Risk: Index-push workflows can notify search engines about URLs and should not be run unintentionally.

Mitigation: Confirm each live index-push submission URL-by-URL and keep dry-run behavior unless the user explicitly approves live submission.

Risk: Locally saved audit outputs may contain sensitive SEO metrics, crawl results, or business context.

Mitigation: Store audit outputs only in approved workspace locations and avoid persisting confidential metrics unless the user requests it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/technical-seo-checker)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Bulk Audit Playbook](references/bulk-audit-playbook.md)
- [E-commerce Platform Patterns](references/ecommerce-platform-patterns.md)
- [HTTP Status Codes](references/http-status-codes.md)
- [LLM Crawler Handling](references/llm-crawler-handling.md)
- [Pre-Migration Playbook](references/pre-migration-playbook.md)
- [Robots.txt Reference](references/robots-txt-reference.md)
- [Technical Audit Example](references/technical-audit-example.md)
- [Technical Audit Templates](references/technical-audit-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit report with scored findings, prioritized recommendations, checklists, and occasional inline shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include measured, user-provided, estimated, or N/A labels for metrics; may include a handoff summary suitable for storage in the user's SEO workflow.]

## Skill Version(s):

19.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
