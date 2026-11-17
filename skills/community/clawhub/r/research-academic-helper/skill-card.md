## Description:

本技能专为学术研究者设计，支持论文润色、文献综述生成、创新点提炼三大核心功能，支持中英文双语，并可在启用联网后检索最新文献。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Academic researchers, graduate students, and research writers use this skill to polish Chinese or English manuscripts, build literature review frameworks, extract research contributions, and organize literature from uploaded documents or prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded drafts, reviewer comments, grant ideas, patent-sensitive material, or private datasets may contain confidential research information.

Mitigation: Use the skill only in an agent environment approved for that data, and avoid sharing sensitive unpublished material unless the environment's data handling is acceptable.

Risk: Online literature search queries may reveal research interests to external services when networking is enabled.

Mitigation: Enable online search only for queries that are acceptable to expose outside the local environment.

Risk: Helper scripts can create local report, JSON, or CSV files next to input files.

Mitigation: Run scripts in an appropriate working directory and review generated files before sharing or committing them.

## Reference(s):

- [论文润色标准参考](references/polishing-standards.md)
- [文献综述写作指南](references/literature-review-guide.md)
- [论文创新点分析指南](references/innovation-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured text reports, comparison tables, JSON or CSV files, and shell commands when helper scripts are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may create local report, JSON, or CSV files next to user-provided inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
