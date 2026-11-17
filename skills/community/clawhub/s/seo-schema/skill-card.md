## Description:

Detect, validate, and generate Schema.org structured data, with JSON-LD preferred for schema, structured data, rich results, JSON-LD, and markup tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and content teams use this skill to audit existing structured data, identify deprecated rich-result markup, and generate implementation-ready JSON-LD snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked broadly by the word "markup" and may produce SEO reports or JSON-LD files when the user intended a different markup task.

Mitigation: Confirm the task is about structured data or rich-result markup before creating files or schema output.

Risk: Generated schema can become misleading if Google rich-result policies have changed or if placeholders are published without review.

Mitigation: Review generated JSON-LD against current search documentation and replace all placeholders with truthful, verifiable page data before publishing.

## Reference(s):

- [Deprecated Schema.org rich result types (2024-2026)](references/deprecated-types-2024-2026.md)
- [ClawHub seo-schema Skill Page](https://clawhub.ai/asale-ai/skills/seo-schema)
- [Google Search rich result retirement announcement](https://developers.google.com/search/blog/2025/06/simplifying-search-results)
- [Google HowTo and FAQ changes](https://developers.google.com/search/blog/2023/08/howto-faq-changes)
- [Google FAQPage structured data documentation](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and JSON-LD code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose SCHEMA-REPORT.md and generated-schema.json files when an agent is working in a writable project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
