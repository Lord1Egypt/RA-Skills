## Description: <br>
Export WeChat public account articles as mobile long screenshots (PNG), PDFs, or high-quality Markdown with YAML frontmatter and code block support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benzking](https://clawhub.ai/user/benzking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to export a user-provided WeChat article URL into local reading, archive, or editing artifacts. It supports screenshot, PDF, and Markdown workflows, including optional local image downloads for Markdown exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided WeChat article content and may download embedded remote images. <br>
Mitigation: Use trusted article URLs and run with --no-images when local copies of remote images are not needed. <br>
Risk: Exports create persistent local copies of article content in the chosen output directory. <br>
Mitigation: Choose an output directory appropriate for retained article copies and review files before sharing or committing them. <br>
Risk: The skill runs headless Chromium with anti-automation settings to render article pages. <br>
Mitigation: Run it in an isolated workspace and confirm that this access pattern is acceptable for the target content and environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benzking/wechat-article-export) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown with file paths for generated PNG, PDF, and Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports selectable export formats, optional image downloading, and optional YAML frontmatter.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
