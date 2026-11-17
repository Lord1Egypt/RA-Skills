## Description:

Publish content directly to WordPress sites via REST API with full Gutenberg block support, including post and page publishing, category selection, SEO tag generation, preview workflows, and Markdown or HTML conversion to Gutenberg blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

GPL v3

## Use Case:

Developers, content teams, and site operators use this skill to prepare, preview, publish, update, schedule, and verify WordPress content through the WordPress REST API. It is intended for workflows that need Gutenberg block output from Markdown or HTML and managed category/tag handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful WordPress credentials and can publish or modify live content.

Mitigation: Use a dedicated least-privileged WordPress account, avoid passing application passwords on the command line, and confirm every live publish, update, or delete action.

Risk: Generated or imported content may include untrusted HTML or links that could create site security or content-integrity issues.

Mitigation: Publish drafts first, review previews, and sanitize untrusted HTML and links before approving publication.

Risk: Incorrect category, tag, scheduling, or status choices can expose content prematurely or place it in the wrong site context.

Mitigation: Use draft or pending status for review, verify category and tag selections, and check scheduled publication dates before changing content status.

## Reference(s):

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Gutenberg Block Reference](https://developer.wordpress.org/block-editor/reference-guides/core-blocks/)
- [Gutenberg Blocks Reference](references/gutenberg-blocks.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with Python and shell command examples, plus generated Gutenberg block markup for WordPress content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify WordPress posts, pages, categories, tags, and media when used with valid WordPress credentials.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
