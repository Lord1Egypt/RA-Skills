## Description:

Helps agents draft, edit, and format WeChat public-account articles using structured Markdown, required title and digest metadata blocks, and 40 advanced layout modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suenkv](https://clawhub.ai/user/suenkv)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketing teams, and agents use this skill to plan and write WeChat public-account articles with reusable article structures, Markdown elements, and custom fenced layout modules. It is suited for long-form posts, brand announcements, tutorials, proposals, product descriptions, case studies, and campaign articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated public-facing article content, links, public-account IDs, or external image URLs may be inaccurate or unsuitable for publication.

Mitigation: Review the full article, links, account identifiers, and image URLs before publishing to WeChat.

Risk: Incorrect custom fenced-block syntax or module fields can produce rendering failures or malformed WeChat layout output.

Mitigation: Check generated module names, required fields, pipe-delimited columns, and four-colon delimiters against the module reference before conversion.

## Reference(s):

- [Wechat Article Writer V2 on ClawHub](https://clawhub.ai/suenkv/skills/wechat-article-writer-v2)
- [Publisher profile: suenkv](https://clawhub.ai/user/suenkv)
- [WeChat layout module reference](references/module_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown using standard Markdown plus custom four-colon fenced blocks for WeChat article metadata and layout modules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated articles should include explicit title and digest metadata blocks; public-facing content, links, public-account IDs, and external image URLs should be reviewed before publishing.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog mention 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
