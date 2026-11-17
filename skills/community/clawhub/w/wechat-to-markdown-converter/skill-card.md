## Description:

This skill converts public WeChat Official Account article pages into clean Markdown with metadata, code blocks, rich text, and optional local image assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzking](https://clawhub.ai/user/benzking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to convert public mp.weixin.qq.com article URLs into Markdown for extraction, saving, or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching and image downloading are broader than the claimed WeChat-only scope.

Mitigation: Use only trusted WeChat article URLs, prefer --no-images for untrusted pages, choose a contained output directory, and run the skill in an isolated environment.

Risk: Remote page and image downloads may follow redirects or fetch unexpected content.

Mitigation: Before low-risk use, add strict host allowlisting, redirect and IP validation, download size limits, and pinned dependencies.

Risk: Conversion can fail or omit content for captcha pages, login-gated articles, or code rendered as images or SVG.

Mitigation: Use public article URLs, retry later after captcha challenges, and review generated Markdown against the source article.

## Reference(s):

- [WeChat DOM Reference](references/wechat-dom-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/benzking/skills/wechat-to-markdown-converter)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Code, Guidance]

**Output Format:** [Markdown files with YAML frontmatter, local image links, shell commands, and Python API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an article directory with a Markdown file and images/ assets; supports --no-images, --no-frontmatter, --no-playwright, and --obsidian.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
