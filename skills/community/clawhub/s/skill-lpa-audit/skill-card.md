## Description:

提供LPA分层审核全流程支持，包括知识库查询、标准清单生成、结果录入分析、报告汇总生成；当需要进行分层审核培训、执行审核任务、分析审核数据或制作审核报告时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality teams, manufacturing engineers, and auditors use this skill to plan layered process audits, generate audit checklists, analyze audit results, and prepare structured LPA reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute unescaped content from audit result data.

Mitigation: Review and sanitize audit result JSON from other people or untrusted systems; avoid opening generated HTML reports in privileged browser sessions or hosting them in authenticated sites until dynamic fields are escaped.

Risk: The skill writes files to user-directed local paths.

Mitigation: Run scripts in a dedicated workspace and review output paths before execution to avoid overwriting important local files.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-lpa-audit)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-lpa-audit)
- [Audit Levels Reference](references/audit_levels.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON analysis and HTML report file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language audit guidance; scripts write user-directed local output files.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
