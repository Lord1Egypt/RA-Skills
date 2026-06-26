## Description: <br>
Fetches public WeChat article pages and converts them into Obsidian-compatible Markdown, with optional image downloads and formatting cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuiilabs](https://clawhub.ai/user/kuiilabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge-base users use this skill to save public WeChat articles into local Obsidian-compatible Markdown files, including article metadata and optional local image assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided WeChat pages and images over the network. <br>
Mitigation: Install and run it only when that network access is expected, and use --no-images if local asset downloads are not needed. <br>
Risk: The skill writes Markdown and image files into a local Obsidian output directory. <br>
Mitigation: Run it first against a dedicated output directory and review generated files before moving them into a primary knowledge base. <br>
Risk: Articles with the same cleaned title can overwrite existing output. <br>
Mitigation: Check the destination folder for same-title articles or use a separate output directory for each batch. <br>


## Reference(s): <br>
- [WeChat Saver Usage Guide](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kuiilabs/wechat-saver) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, local image files, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process one or more user-provided WeChat article URLs; images can be skipped with --no-images.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
