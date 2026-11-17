## Description:

中小学教师智能备课助手可帮助教师生成课件、教学设计、学生任务单、参考资料清单、辅助教学 HTML 工具和思维导图等成套备课材料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahao2001](https://clawhub.ai/user/ahao2001)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and teaching-support agents use this skill to prepare complete primary and secondary school lesson packages, including classroom presentation materials, lesson plans, student worksheets, diagrams, and supporting resource records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores education-platform credentials in plaintext workspace configuration.

Mitigation: Use a secure credential manager before entering passwords, or skip account setup until credential handling is changed.

Risk: The skill describes broad automatic actions, including downloads and cleanup of generated script files.

Mitigation: Run only in a contained workspace and require explicit user confirmation before downloading resources or deleting files.

Risk: The installation flow describes persistent global memory shortcuts.

Mitigation: Remove or narrow global shortcut entries before installation so activation is explicit and scoped.

Risk: Diagram integration references MCP/npm behavior that may depend on unpinned packages.

Mitigation: Pin and review any MCP or npm dependency before enabling diagram generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ahao2001/skills/teacher-ai-preparing-lesson)
- [PPT Guide](artifact/references/ppt_guide.md)
- [Mindmap Guide](artifact/references/mindmap_guide.md)
- [Teaching Design Template v2](artifact/references/teaching_design_template_v2.md)
- [Task Sheet Template v2](artifact/references/task_sheet_template_v2.md)
- [Education Resource Platforms](artifact/references/edu_platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated lesson-prep files such as PPTX, DOCX, HTML, Mermaid, JSON, and resource-list Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized under a MyTeacher course folder and may depend on companion document, presentation, and diagram skills.]

## Skill Version(s):

2.1.1 (source: server release metadata; artifact frontmatter reports 2.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
