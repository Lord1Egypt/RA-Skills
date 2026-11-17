## Description:

SERP Markup Builder helps agents generate optimized page-head assets, including title and meta description options, Open Graph and Twitter tags, canonical and robots tags, and Schema.org JSON-LD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, SEO practitioners, and developers use this skill to produce page-head metadata packages and structured data for search result presentation, social sharing, and answer-engine eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent host to run an undeclared local Python preflight command against user-supplied URLs.

Mitigation: Prefer the declared WebFetch path when possible; if the preflight is used, validate URLs first and run the command with argument-array execution in a trusted connector environment.

Risk: The referenced schema_lint.py connector may be absent or untrusted in the installing agent host.

Mitigation: Confirm the connector exists, is expected for the host, and has been reviewed before allowing the skill to invoke it.

Risk: Generated JSON-LD, review data, prices, ratings, dates, or author fields could misrepresent a page if unsupported by visible content.

Mitigation: Require generated schema properties to map to visible page content or user-provided facts, and omit unverifiable review, rating, price, date, or author values.

Risk: Locale examples and memory-write paths may not match the user's site, language, or workflow.

Mitigation: Adjust locale assumptions and storage destinations to the specific site and agent workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/serp-markup-builder)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [CTR Optimization and Social Tags Reference](references/ctr-and-social-reference.md)
- [Meta Tags Optimizer Detailed Instructions](references/meta-instructions-detail.md)
- [Meta Tag Code Templates](references/meta-tag-code-templates.md)
- [Meta Tag Formulas Reference](references/meta-tag-formulas.md)
- [Schema Type Decision Tree](references/schema-decision-tree.md)
- [Schema Markup Generator Detailed Instructions](references/schema-instructions-detail.md)
- [Schema.org JSON-LD Templates](references/schema-templates.md)
- [Schema Markup Validation Guide](references/validation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML meta tag snippets, JSON-LD code blocks, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clearly labeled placeholders for facts that must be confirmed against visible page content.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
