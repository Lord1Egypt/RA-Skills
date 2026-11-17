## Description:

This skill converts WeChat Official Account article pages into clean Markdown, with support for article metadata, rich text, code blocks, tables, and optional image downloading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzking](https://clawhub.ai/user/benzking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content archivists use this skill to convert public WeChat Official Account articles into Markdown files or inline Markdown for review, extraction, and archiving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs with outbound network access.

Mitigation: Use it only with trusted WeChat article URLs and avoid untrusted or non-WeChat links until host allowlisting is enforced.

Risk: Remote pages are rendered with Chromium sandboxing disabled.

Mitigation: Run the skill in a sandboxed or containerized environment with limited host access.

Risk: The skill writes Markdown and optional downloaded image files to a local output directory.

Mitigation: Choose a dedicated output directory and review generated files before reusing or publishing them.

## Reference(s):

- [WeChat DOM Reference](references/wechat-dom-reference.md)

## Skill Output:

**Output Type(s):** [markdown, files, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files with optional YAML frontmatter, local image files, and inline Python return data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI conversion writes an article directory containing a Markdown file and optional images; programmatic conversion returns Markdown, metadata, code block details, and image URLs.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
