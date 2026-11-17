## Description:

内容引擎 / Content Engine helps agents create, adapt, schedule, publish, and analyze Markdown-native content across Twitter/X, LinkedIn, WeChat Official Account, blogs, Medium, and Obsidian workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, and developers use this skill to manage a local content pipeline, adapt drafts to multiple publishing platforms, generate image prompts, plan calendars, and review performance metrics before or after publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Obsidian import and export workflows can read or overwrite files outside the intended vault.

Mitigation: Review or disable Obsidian workflows before installation, restrict vault paths, and require explicit confirmation before import, export, sync, or file overwrite actions.

Risk: Publishing, scheduling, deletion, and export actions can affect public channels or local content.

Mitigation: Use least-privilege platform tokens and require a preview plus explicit user confirmation before public publish, schedule, delete, export, or overwrite actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanjing5024064/skills/smart-content-engine)
- [Platform Specifications](references/platform-specs.md)
- [WeChat Guide](references/wechat-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, generated content drafts, platform-specific adaptations, JSON-style action inputs, reports, and local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional platform credentials from environment variables and stores content data locally.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
