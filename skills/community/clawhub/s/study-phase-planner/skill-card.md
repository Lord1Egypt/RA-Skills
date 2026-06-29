## Description: <br>
生成面向小学、初中、高中和大学学习者的三阶段学习或复习计划，并输出含里程碑检查点的交互式中文 HTML 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and learning-support users use this skill to plan Chinese-language study, revision, or exam-preparation schedules across common education stages and subjects. It structures the plan into foundation, reinforcement, and sprint phases with measurable milestones and an HTML progress report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad study-planning requests and produce a report before enough context is available. <br>
Mitigation: Confirm the education stage, grade, subject, target type, and available time window before generating the plan. <br>
Risk: Generated HTML reports may contain personal study details and may be updated in place during revisions. <br>
Mitigation: Store reports in an appropriate local workspace, review the contents before sharing, and keep a separate copy when preserving earlier versions matters. <br>


## Reference(s): <br>
- [中国教育阶段与学科参考数据](artifact/references/education_stages.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Chinese-language planning guidance plus an interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local HTML report under output/ and may update the report during revisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
