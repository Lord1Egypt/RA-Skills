## Description: <br>
Helps independent teachers turn schedule, student, homework, parent communication, and lesson-package data into a daily dashboard with priority follow-ups and objective student risk flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Independent teachers use this skill to generate a daily operating dashboard covering today's classes, preparation, post-class feedback, homework follow-up, parent communication, lesson packages, and the three most important actions. It reads existing workspace data, highlights risks from objective fields, and keeps external communication or writes pending teacher confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation could read student, parent, homework, or course-hour workflow data for generic planning requests. <br>
Mitigation: Use explicit teacher-workbench prompts and add confirmation before reading sensitive workspace data for generic requests such as daily planning. <br>
Risk: Dashboard output could expose sensitive student or parent details. <br>
Mitigation: Use aliases, omit direct identifiers, keep parent and fact summaries within the documented 500-character cap, and avoid family, medical, financial, contact, or identity details. <br>
Risk: Student risk flags could be misleading if based on impressions rather than data. <br>
Mitigation: Base risk flags on documented objective thresholds, cite the source field evidence, and explicitly label any teacher-provided subjective judgment. <br>
Risk: Suggested parent communication or record updates could be mistaken for automatic actions. <br>
Mitigation: Keep messages, lesson-log summaries, renewal suggestions, and course-hour changes as drafts that require teacher confirmation before any external action or write. <br>


## Reference(s): <br>
- [Dashboard Template](references/dashboard-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qizhitang/xiaozhi-teach-solo-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown dashboard with structured text tables, checklists, prioritized actions, and risk explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses aliases for students, cites objective fields for risk flags, and does not automatically send parent messages or write records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
