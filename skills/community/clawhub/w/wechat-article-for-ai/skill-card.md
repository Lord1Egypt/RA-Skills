## Description:

Convert WeChat Official Account articles to clean Markdown files with locally downloaded images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soar999](https://clawhub.ai/user/soar999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and AI agents use this skill to convert WeChat Official Account articles into reusable Markdown, including article metadata, code blocks, media references, and optional local image copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad network access and file-writing behavior can affect unintended local paths or services.

Mitigation: Run the skill in a sandbox or low-privilege environment and set a dedicated output directory for generated Markdown, images, and debug HTML.

Risk: Article-controlled image URLs may trigger requests to unintended internal or external services.

Mitigation: Avoid processing untrusted article URLs with image downloads enabled; use --no-images for unknown content.

Risk: Runtime dependencies and the Camoufox browser artifact are downloaded or loaded outside the skill source.

Mitigation: Pin and review dependencies and the Camoufox browser artifact before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soar999/skills/wechat-article-for-ai)
- [Camoufox project](https://github.com/nichochar/camoufox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter and local image assets; MCP tools return text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-article output directories, supports batch conversion, and can skip local image downloads with --no-images.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
