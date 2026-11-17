## Description:

Helps math teachers design diagnostic, formative, and summative assessments with blueprints, question-selection guidance, and item-level analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

Math teachers use the skill to plan middle and high school assessments, prepare blueprints and question-selection criteria, and review item-level results. Teachers verify drafted questions and confirm any class-workspace updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment was partial and noted a possible inconsistency in the student report sample.

Mitigation: Review the student report sample before relying on it, and treat the security assessment as incomplete.

Risk: The assessment workflow can involve student records and confidential exam materials.

Mitigation: Use only the minimum permitted class information and do not provide unreleased exam questions, answer keys, or scoring rubrics.

Risk: AI-generated candidate questions may contain errors.

Mitigation: Independently solve and check each draft; keep it out of the final assessment until a teacher verifies it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-math-exam-designer)
- [Publisher profile](https://clawhub.ai/user/qizhitang)
- [Assessment design process](artifact/references/exam-design-process.md)
- [Blueprint template](artifact/references/blueprint-template.md)
- [Result analysis rubric](artifact/references/result-analysis-rubric.md)
- [Class teaching workspace schema](artifact/shared/class-teaching-workspace.schema.json)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown tables and prose; structured JSON fields for teacher-confirmed workspace updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Question drafts require teacher verification before inclusion in an assessment.]

## Skill Version(s):

2.12.7 (source: frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
