## Description:

Generate URL-friendly slugs from text, including mixed Chinese and English input, special-character filtering, custom separators, and multiple output cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and site maintainers use this skill to create URL-safe slugs for blogs, e-commerce listings, CMS pages, and permalinks from mixed Chinese and English text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Chinese-to-pinyin mapping is small, so generated slugs may be incomplete or inaccurate for broader Chinese text.

Mitigation: Review generated slugs before publishing and expand or replace the mapping for production content workflows that need broad Chinese coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/slug-generator)
- [Publisher profile](https://clawhub.ai/user/darbling)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON from the local Python script, with Markdown usage guidance in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slug output depends on the input text, separator, and case option.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
