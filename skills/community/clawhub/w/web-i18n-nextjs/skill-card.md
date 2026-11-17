## Description:

Internationalization (i18n) guide for Next.js and Node.js web applications using the App Router, covering translation file structure, locale routing, SEO metadata, hreflang, JSON-LD, UI translations, and multi-language sitemaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

Developers and web engineers use this skill to add or maintain internationalization in Next.js App Router applications, including locale-aware translations, routing, metadata, structured data, and sitemaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags one JSON-LD example as unsafe when dynamic CMS or translation-controlled content is inserted into script tags.

Mitigation: Use an HTML-safe JSON serializer or equivalent escaping before rendering dynamic JSON-LD in script tags.

Risk: The skill assumes English clean URLs as the root/default locale convention.

Mitigation: Confirm the project's default-locale URL policy and adjust examples when English should not be the unprefixed root locale.

## Reference(s):

- [Translation Files Reference](references/translation-files.md)
- [Routing & Middleware Reference](references/routing.md)
- [SEO Metadata Reference](references/seo-metadata.md)
- [Structured JSON-LD Data Reference](references/structured-data.md)
- [Multi-Language Sitemap Reference](references/sitemap.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, JSON, and XML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on implementation checklists and project-specific adaptation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
