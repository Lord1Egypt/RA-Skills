## Description: <br>
Xiaozhi Teach Assignment Designer helps teachers create differentiated homework, grading rubrics, and feedback templates from lesson goals and available learning diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to turn lesson topics, existing homework, or class learning summaries into layered assignment cards, scoring standards, and concise feedback templates. It supports differentiated practice while defaulting to a basic assignment when no learning profile is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use learning summaries or assignment results that contain sensitive student information. <br>
Mitigation: Use anonymized or aggregate inputs unless the connected school systems are approved for identifiable student data. <br>
Risk: Layered assignments can be misleading if A/B/C grouping is generated without current learning evidence. <br>
Mitigation: Use teacher-supplied diagnostics or the connected student-analyzer output for layering; otherwise keep the documented basic assignment mode. <br>
Risk: Generated rubrics and feedback may not match local grading policies or individual accommodations. <br>
Mitigation: Have the teacher review scoring standards, workload, and feedback language before assigning work to students. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qizhitang/xiaozhi-teach-assignment-designer) <br>
- [Assignment rubric template](references/assignment-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with structured assignment cards, grading rubrics, and feedback templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use anonymized class or student learning summaries when supplied; otherwise defaults to a basic assignment.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
