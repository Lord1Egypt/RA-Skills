## Description: <br>
Helps math teachers turn wrong-answer records into systematic error-cause analysis, knowledge-map insights, class and student profiles, and teaching intervention recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Math teachers use this skill to classify student and class math errors into seven cause categories, connect them to knowledge-map gaps, and draft targeted class-wide and individual teaching interventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student error analysis may expose unnecessary personally identifying student details if raw names or full student records are provided. <br>
Mitigation: Use pseudonyms or student IDs, provide only the error data needed for analysis, and avoid publishing real names with wrong-answer records. <br>
Risk: Teaching recommendations may be over-relied on as final grading, ranking, or instructional decisions. <br>
Mitigation: Use the output as teacher-facing diagnostic support only; teachers should review results before grading, ranking, or changing instruction. <br>
Risk: Broad activation wording may route general teaching prompts into this diagnostic workflow when a narrower response is intended. <br>
Mitigation: Confirm the user wants math error-cause analysis before applying the full diagnostic workflow to broad teaching prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qizhitang/xiaozhi-teach-math-error-analyzer) <br>
- [Error classification rubric](references/error-classification-rubric.md) <br>
- [Intervention design template](references/intervention-design.md) <br>
- [Knowledge map template](references/knowledge-map-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, rubrics, knowledge maps, and intervention recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Teacher-facing outputs should use pseudonymized student identifiers and remain advisory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
