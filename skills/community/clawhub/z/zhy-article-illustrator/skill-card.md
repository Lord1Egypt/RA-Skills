## Description:

Use when illustrating a Markdown article with high-finish editorial visuals, visual-bible planning, structured prompts, optional Qiniu upload, and inserted image references for article publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhylq](https://clawhub.ai/user/zhylq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to add planned editorial illustrations to Markdown articles. It analyzes article structure, creates a visual bible and outline, generates prompts and images, optionally uploads images to Qiniu, and writes an illustrated article copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content, reference images, and API keys may be sent to the configured image generation endpoint, including the default third-party relay reported by the security scan.

Mitigation: Set IMAGE_BASE_URL or XIAOMI_BASE_URL to a trusted official or self-controlled endpoint before use, and avoid running the skill on confidential drafts or private reference images.

Risk: Passing API keys on the command line can expose credentials through shell history or process listings.

Mitigation: Provide credentials through environment variables or a local .env file, and avoid using the --api-key argument.

Risk: Optional Qiniu upload can transmit generated images to the configured storage bucket and expose them through the configured CDN domain.

Mitigation: Enable upload only when the Qiniu bucket, domain, and access policy are approved for the article content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhylq/skills/zhy-article-illustrator)
- [config-schema.md](artifact/references/config-schema.md)
- [prompt-guide.md](artifact/references/prompt-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, generated Markdown files, structured prompts, image files, JSON summaries, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce an illustrated article copy, visual-bible.md, outline.md, prompt files, PNG images, optional CDN URLs, and success/failure counts.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
