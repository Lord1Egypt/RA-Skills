## Description:

Evaluates frontend and backend PDF resumes with Claude and produces an HTML report with scores, section feedback, and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifenglei](https://clawhub.ai/user/lifenglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, job seekers, and resume reviewers use this skill to evaluate PDF resumes for frontend or backend roles and generate a local HTML report with structured improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume text, including contact and employment details, is sent to Claude for analysis.

Mitigation: Use only when that data sharing is acceptable, and redact sensitive fields before running the skill when possible.

Risk: The generated HTML report contains resume details and model-produced recommendations.

Mitigation: Review the local HTML report before sharing it or acting on its recommendations.

Risk: Dependency versions are not pinned in the artifact requirements file.

Mitigation: Pin dependency versions before reproducible or production installation.

## Reference(s):

- [Backend Resume Evaluation Criteria](references/backend-evaluation.md)
- [Frontend Resume Evaluation Criteria](references/frontend-evaluation.md)

## Skill Output:

**Output Type(s):** [text, code, guidance, files]

**Output Format:** [HTML report generated from Claude JSON analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is written as a local HTML file and may contain resume details from the submitted PDF.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
