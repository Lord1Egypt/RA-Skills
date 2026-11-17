## Description:

帮独立教师记录课上练习和学员带来的学校作业、整理错因与完成状态，并据此准备下一节课的关注重点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

独立教师用它跟踪课上练习和学员带来的学校作业、考试错题，归纳可跟进的错因，并整理下一节课的教学关注点。它保留判分和面向学员或家长的沟通给老师处理。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports two moderate scope mismatches, and Skillspector coverage is partial because three local references could not be resolved.

Mitigation: Review the reported scope mismatches and check the unresolved references before installing; the benign verdict has medium confidence and the evidence is incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-homework-tracker)
- [错误原因词表与弱项阈值](artifact/shared/vocab.md)
- [完成度追踪视图模板](artifact/references/completion-tracking-views.md)
- [错题回流清单模板](artifact/references/error-reflow-checklist-template.md)
- [危机例外处置](artifact/shared/crisis-exception.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Text summaries and Markdown reports, with structured workspace fields represented in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses aliases and records completion status, error dimensions, knowledge points, and follow-up actions; does not store assignment text or answers.]

## Skill Version(s):

2.12.7 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
