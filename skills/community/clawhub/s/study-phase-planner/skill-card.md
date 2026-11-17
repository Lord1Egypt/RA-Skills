## Description:

学习阶段计划生成器，为小学、初中、高中和大学各阶段各学科制定基础、强化、冲刺三阶段学习计划，包含里程碑检查点和交互式 HTML 可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, tutors, and external ClawHub users use this skill to create Chinese study, revision, or exam-preparation plans across school stages and subjects. It structures the plan into foundation, reinforcement, and sprint phases with measurable milestones and an HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated study reports are active HTML, and untrusted markup in plan fields could affect what runs or displays when a report is opened in a browser.

Mitigation: Use trusted learner inputs, review generated report content before opening or sharing it, and prefer a hardened release that escapes template values before rendering HTML.

## Reference(s):

- [中国教育阶段与学科参考数据](references/education_stages.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/study-phase-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese planning guidance with generated local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an HTML template with timeline, phase details, milestone cards, checkpoint rows, and study tips.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
