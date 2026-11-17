## Description:

辅助APQP项目管理全流程；支持项目阶段定义、文档生成（FMEA/PPAP/控制计划）、甘特图可视化、风险分析与知识库查询；适用于制造业产品质量规划全流程

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing quality teams, APQP project managers, and design/process engineers use this skill to plan APQP phases, generate FMEA, control-plan, PPAP, and Gantt artifacts, and review project risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Gantt HTML can run unsafe content when crafted project names or phase JSON are used.

Mitigation: Use only trusted input for Gantt generation, avoid opening generated HTML from untrusted data, and prefer a fixed version with HTML escaping and phase JSON validation.

Risk: Generated artifacts can overwrite existing files when output paths are reused.

Mitigation: Verify output paths before running scripts and write generated files to a dedicated project output directory.

Risk: FMEA, PPAP, and control-plan outputs may not reflect customer-specific requirements without review.

Mitigation: Have qualified project, quality, and customer-facing reviewers check generated deliverables before submission or production use.

## Reference(s):

- [APQP阶段详细指南](artifact/references/apqp_phases.md)
- [IATF 16949 标准要点](artifact/references/iatf16949_knowledge.md)
- [APQP最佳实践](artifact/references/best_practices.md)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-apqp-project-manager)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-apqp-project-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell-command examples, JSON checklists and status, Markdown reports, and HTML Gantt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated APQP deliverables depend on user-provided project, product, customer, and schedule data and should be reviewed against customer-specific requirements.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
