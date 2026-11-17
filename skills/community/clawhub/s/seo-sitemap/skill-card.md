## Description:

Analyze existing XML sitemaps or generate new ones with industry templates, validating format, URLs, and structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, developers, and site operators use this skill to inspect existing XML sitemaps, identify structural or URL-level issues, and generate valid sitemap files with supporting site-structure documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sitemap analysis may fetch public URLs for sites the user provides.

Mitigation: Run the skill only for sites the user intends to inspect and review fetched URL targets before relying on the results.

Risk: Search Console checks can expose account or property data if used with the wrong credentials.

Mitigation: Use Search Console commands only with accounts and properties the user intentionally authorizes.

Risk: Generated sitemap or SEO recommendations may include misleading large-scale page patterns if used without review.

Mitigation: Review generated sitemap structure, location-page volume, and unique-content guidance before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-sitemap)
- [Sitemaps XML schema](http://www.sitemaps.org/schemas/sitemap/0.9)
- [Google image sitemap schema](http://www.google.com/schemas/sitemap-image/1.1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with XML examples, shell commands, validation reports, recommendations, sitemap files, and structure documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local report files such as VALIDATION-REPORT.md, sitemap.xml or split sitemap files, and STRUCTURE.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
