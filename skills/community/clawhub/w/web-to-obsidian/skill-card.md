## Description:

抓取网页文章并保存到 Obsidian vault。当用户想要保存网页文章、博客、文档到 Obsidian 时使用，特别是提到"保存到 Obsidian"、"存到 Obsidian"、"抓取网页"、"网页转 Obsidian"、"导入文章"等场景。支持自动翻译非中文内容为中文，生成元数据（标签、摘要、标题），并以 Obsidian Markdown 格式存储。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ioriiod0](https://clawhub.ai/user/ioriiod0)

### License/Terms of Use:


## Use Case:

Developers, researchers, and knowledge workers use this skill to fetch web articles, blogs, and documentation, optionally translate non-Chinese content into Chinese, generate metadata, and save the result as an Obsidian-ready Markdown note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URLs and fetched content may be sent to third-party conversion services.

Mitigation: Avoid private, internal, signed, tokenized, or sensitive URLs unless the user explicitly accepts external URL forwarding.

Risk: Weak transport security can reduce confidence in fetched content integrity.

Mitigation: Review fetched Markdown before importing it into Obsidian and prefer trusted sources.

Risk: Imported or translated content may be inaccurate or misleading.

Mitigation: Ask the user to review translated text, metadata, and generated tags before relying on the saved note.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ioriiod0/skills/web-to-obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Obsidian-compatible Markdown with YAML frontmatter, plus shell commands and user-facing status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a temporary Markdown file before importing the note into an Obsidian vault.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
