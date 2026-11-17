## Description:

Website SEO Optimizer analyzes HTML/CSS sites for SEO issues, generates audit reports, and guides fixes for metadata, headings, images, structured data, robots.txt, and sitemaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to audit static HTML/CSS websites, prioritize SEO fixes, add structured metadata, generate sitemap files, and prepare robots.txt configuration before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SEO, language, locale, or schema guidance may not match the site's real content or target audience.

Mitigation: Review generated changes before publishing and choose language, locale, and structured-data values that accurately describe the site.

Risk: Sitemap generation can replace an important existing output file if pointed at the same path.

Mitigation: Check the intended sitemap output path before running the generator and keep backups for existing production files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yesong-hue/skills/website-seo-optimizer)
- [SEO Optimization Checklist](references/seo_checklist.md)
- [Schema Markup Guide](references/schema_markup_guide.md)
- [Robots.txt Template](assets/robots.txt)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML and JSON-LD snippets, shell commands, text or JSON SEO reports, robots.txt configuration, and XML sitemap output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or replace sitemap output files when the sitemap script is run; review generated SEO changes before publishing.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
