## Description:

Helps agents integrate Schema.org structured data into websites for rich search results, better SEO, and improved communication with search engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kxrbx](https://clawhub.ai/user/kxrbx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add Schema.org JSON-LD to web pages and produce structured data snippets for common site content such as FAQ pages, articles, products, local businesses, events, and organizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML injection helper can create cross-site scripting exposure when JSON-LD contains untrusted user-supplied or CMS-supplied content.

Mitigation: Escape script-breaking characters or parse and re-serialize JSON-LD safely before publishing generated HTML.

Risk: Generated structured data can become inaccurate or misleading if page-specific inputs are incomplete or stale.

Mitigation: Review generated schema content against the live page content before deployment.

## Reference(s):

- [Schema.org](https://schema.org)
- [ClawHub skill page](https://clawhub.ai/kxrbx/skills/schemaorg-site-enhancer)
- [Publisher profile](https://clawhub.ai/user/kxrbx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, JSON-LD, and HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated JSON-LD should be reviewed before publishing when page content comes from users or a CMS.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
