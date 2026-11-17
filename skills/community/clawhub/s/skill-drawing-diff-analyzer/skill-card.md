## Description:

自动对比2D图纸与3D模型的尺寸、轮廓差异；输出JSON和Markdown格式差异报告；支持直径符号和几何公差识别；适用于设计评审阶段快速发现图纸不一致问题

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Design reviewers, CAD engineers, and manufacturing or quality teams use this skill to compare 2D engineering drawings against 3D models during design review and produce discrepancy reports for human assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CAD, PDF, and model parsing dependencies may introduce environment or supply-chain risk.

Mitigation: Install dependencies in an isolated virtual environment or container and prefer reviewed, pinned package versions.

Risk: Drawing comparison reports may be incomplete or misleading for geometric tolerances and critical engineering decisions.

Mitigation: Treat outputs as review aids and manually verify geometric tolerances, critical differences, and final engineering conclusions.

Risk: Generated Markdown may reflect unescaped input metadata.

Mitigation: Review generated Markdown before sharing it or rendering it in trusted systems.

## Reference(s):

- [图纸格式指南](references/format-guide.md)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-drawing-diff-analyzer)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-drawing-diff-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated reports are JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default comparison tolerance is 0.1 mm and can be adjusted with --tolerance]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
