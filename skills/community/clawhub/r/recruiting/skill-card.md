## Description:

Hiring workflow management with structured processes and candidate tracking for job descriptions, resume screening, interviews, candidate pipelines, and offer-related communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and hiring managers use this skill to structure job descriptions, candidate screening, interview preparation, pipeline tracking, and candidate communications while keeping hiring decisions under human control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applicant data and hiring assessments are stored locally in plaintext files.

Mitigation: Minimize stored personal data, enforce private file permissions, and apply explicit retention and deletion practices.

Risk: Scores, ratings, interview labels, and reject labels could be treated as automated hiring decisions.

Mitigation: Require human review and approval for all candidate disposition changes, and treat assessments as advisory inputs only.

Risk: Structured recruiting workflows can still introduce or preserve hiring bias.

Mitigation: Use consistent criteria, document evidence for decisions, and maintain human oversight at every decision point.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agistack/skills/recruiting)
- [Job Description Creation](references/job-descriptions.md)
- [Resume Screening](references/resume-screening.md)
- [Pipeline Tracking](references/pipeline-tracking.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON-backed local records and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores recruiting records locally in plaintext JSON files under the agent workspace.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
