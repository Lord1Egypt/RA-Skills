## Description:

Analyzes a secondary vocational lesson-plan DOCX template and fills it with generated lesson content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yon-gjun](https://clawhub.ai/user/yon-gjun)

### License/Terms of Use:

MIT

## Use Case:

Teachers use this skill to create a filled lesson-plan document from a DOCX template, lesson topic, and number of class hours. Teacher, class, and textbook details can also be supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An existing output document may be deleted when the skill writes the generated lesson plan.

Mitigation: Back up documents you need and choose a new output filename.

Risk: The security summary flags a concern about whether the execution environment is proportionate to the task.

Mitigation: Review the access needed to read the template and write the output before running the skill.

Risk: The security scan is incomplete because some local references could not be resolved.

Mitigation: Review the template and any referenced local files before use.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/yon-gjun/zhongshan-lesson-plan)
- [ClawHub skill release](https://clawhub.ai/yon-gjun/skills/zhongshan-lesson-plan)

## Skill Output:

**Output Type(s):** [Files, Documents]

**Output Format:** [Filled Microsoft Word (.docx) lesson plan based on the supplied template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the supplied topic and class-hour count; teacher, class, and textbook details are optional.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
