## Description:

标准化管理技术讨论全生命周期：讨论记录 → 决策沉淀 → 架构文档 → 开发规划。支持 Git 版本管理（可选）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ah0210](https://clawhub.ai/user/ah0210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to capture technical discussions, decisions, architecture notes, and development plans as workspace Markdown documents, with optional Git version recording when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes technical discussion records and related planning documents into the workspace, which may later be shared with a repository.

Mitigation: Review generated documents before sharing or publishing the workspace.

Risk: The optional version-recording flow may create Git commits and tags when the user requests it.

Mitigation: Inspect Git status and confirm the version number and release note before using version recording.

## Reference(s):

- [Usage examples](examples.md)
- [ClawHub skill page](https://clawhub.ai/ah0210/skills/tech-discussion-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and concise agent responses with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes discussion artifacts under the configured workspace discussion directory and may create Git commits or tags only when the user requests version recording.]

## Skill Version(s):

0.8.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
