## Description:

Helps WeChat Official Account creators turn topics, notes, links, or AI news into publish-ready Chinese drafts with optional images, WeChat-safe HTML, validation JSON, and draft-box upload support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymz2012](https://clawhub.ai/user/ymz2012)

### License/Terms of Use:

MIT-0

## Use Case:

External WeChat creators, technical bloggers, AI-news writers, product teams, and content operators use this skill to draft, illustrate, validate, and prepare WeChat Official Account articles. It supports original writing, link translation or rewrite, AI news adaptation, pre-publish review, and optional draft-box creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled uploader can use WeChat credentials and create account-side draft-box entries.

Mitigation: Keep credentials in a local .env file, start with DRY_RUN=1, and review the generated article JSON and media paths before setting DRY_RUN=0.

Risk: The workflow can fetch arbitrary URLs and transform source material into public-facing article drafts.

Mitigation: Use trusted URLs, review extracted sources and generated claims, and soften or remove unsupported statistics, policy, financial, medical, or competitive assertions before upload.

Risk: The uploader can upload user-controlled local cover and inline image paths.

Mitigation: Use only intended PNG or JPG files under data/images, check generated paths, and run npm run validate -- --all before draft creation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ymz2012/skills/wechat-official-account-writer)
- [Article Patterns](references/article-patterns.md)
- [Image and Draft Upload Integration](references/image-and-draft-upload.md)
- [Output Checklist](references/output-checklist.md)
- [WeChat Article Workbench README](scripts/wechat-article-workbench/README.md)
- [AIHOT Curated Source](https://aihot.virxact.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, WeChat-safe HTML JSON, image prompts, shell commands, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-box upload JSON requires local image paths and validation before WeChat draft creation; real publishing remains manual.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
