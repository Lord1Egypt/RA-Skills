## Description:

微信公众号文章抓取工具。将微信文章转换为 Obsidian 兼容的 Markdown 格式，支持图片下载、智能格式识别（代码块/列表/引用）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuiilabs](https://clawhub.ai/user/kuiilabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save public WeChat article links into local Obsidian-compatible Markdown notes. It can process one or more article URLs, optionally download images, and generate Markdown with frontmatter, source links, and capture timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary article and embedded image URLs and write downloaded content into local notes without strong URL, domain, size, or path validation.

Mitigation: Process only trusted links, choose an explicit output directory, and prefer --no-images for untrusted articles until stronger validation and limits are added.

Risk: Dependency installation examples include --break-system-packages, which can alter the system Python environment.

Mitigation: Install dependencies in a dedicated virtual environment and avoid --break-system-packages unless the environment is disposable.

## Reference(s):

- [WeChat Saver Usage Guide](references/usage.md)
- [ClawHub skill page](https://clawhub.ai/kuiilabs/skills/wechat-saver)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter, relative image links, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes converted articles to a local output directory and may write downloaded images to an images subdirectory.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
