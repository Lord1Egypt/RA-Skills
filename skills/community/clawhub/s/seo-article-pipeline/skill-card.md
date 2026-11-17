## Description:

End-to-end SEO article pipeline for researching keywords, analyzing competition, writing articles, generating images, fact-checking, assembling blog files, and translating content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nirusan](https://clawhub.ai/user/nirusan)

### License/Terms of Use:


## Use Case:

Blog teams, content operators, and developers use this skill to produce SEO-focused articles from target keywords, including research briefs, drafts, citations, image prompts, assembled blog files, and translated versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated blog content may be committed and pushed to the main branch without an explicit confirmation step.

Mitigation: Review generated files before version-control operations and prefer a draft branch or pull request for publication.

Risk: Keyword research sends target keywords to DataForSEO and Google Suggest and uses DataForSEO credentials from environment variables.

Mitigation: Avoid confidential campaign terms unless third-party lookup is acceptable, and provide credentials only through the expected environment variables.

Risk: SEO articles can contain stale or incorrect factual claims, pricing, statistics, or product details if sources are not verified.

Mitigation: Use the skill's research and fact-check steps to verify claims against authoritative current sources before publishing.

## Reference(s):

- [Article Checklist](references/article-checklist.md)
- [DataForSEO](https://dataforseo.com)
- [ClawHub Skill Page](https://clawhub.ai/nirusan/skills/seo-article-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, frontmatter, research notes, image prompts, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DataForSEO credentials for keyword research and may produce staged blog content, image assets, translations, and proposed git operations.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
