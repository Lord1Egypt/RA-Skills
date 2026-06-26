## Description: <br>
Helps independent teachers track homework completion, route mistakes back into student analysis, and prepare lesson pre-diagnosis from assignment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External independent teachers use this skill to manage homework from assignment through submission, grading status, error review, and next-lesson diagnosis. It supports student and class completion views, persistent weakness tagging, and handoff summaries for related teaching skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation around homework status could cause unintended access to or updates of student-related records. <br>
Mitigation: Install it only where homework tracking and student diagnostics are intended, and require explicit homework or student context before reading or updating linked records. <br>
Risk: Use with real student records can expose sensitive education information if the skill is given more detail than it needs. <br>
Mitigation: Limit inputs and stored outputs to pseudonyms, completion status, submission timing, error categories, and diagnosis summaries; keep answers, real names, and family details out of the workflow. <br>


## Reference(s): <br>
- [Homework Status Template](references/homework-status-template.md) <br>
- [Homework Tracking Template](references/homework-tracking-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured text templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pseudonymous student references and focuses on homework status, error categories, completion trends, and lesson-planning handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
