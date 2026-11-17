## Description:

中文长篇小说创作工作流，用于创建或延续单本书项目、提炼原作或样本文风、规划章节、起草或修订正文、执行章节 preflight、编号检查、质量门、Markdown 交付，并更新本书记忆与连续性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeoleader](https://clawhub.ai/user/aeoleader)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and writing assistants use this skill to manage a Chinese long-form novel project, keep each book isolated, plan and draft chapters, check continuity, and maintain project-specific memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-specific preferences and continuity notes may contain private story material if unrelated documents are placed in the active novel workspace.

Mitigation: Keep unrelated private material outside the active novel workspace and review memory files before sharing a project.

Risk: Generated chapters can drift from confirmed continuity, chapter numbering, or user constraints.

Mitigation: Use the preflight, chapter-numbering check, continuity memory, and quality gates before accepting or publishing drafts.

Risk: Reference texts or samples could lead to overly close reuse of protected expression.

Mitigation: Use the skill's source-material mode to extract structure, facts, and style characteristics without saving identifiable passages or closely imitating protected text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aeoleader/skills/zh-book-writing)
- [Workflow](references/workflow.md)
- [Writing Principles](references/writing-principles.md)
- [Quality Gates](references/quality-gates.md)
- [Book Scaffold Entry Template](assets/book-scaffold/00_入口.md)
- [古风权谋样例](examples/古风权谋样例/00_入口.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown plans, Markdown chapter files, project memory files, and concise status blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains per-book memory and continuity notes inside the active novel workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
