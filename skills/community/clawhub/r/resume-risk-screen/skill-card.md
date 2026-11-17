## Description:

A skill for screening resumes for authenticity risk, packaging risk, and role fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donotwannatry](https://clawhub.ai/user/donotwannatry)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and technical interviewers use this skill to screen candidate resume text for authenticity risks, packaging concerns, role fit, and follow-up interview questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes resumes and contact details.

Mitigation: Use only candidate data the reviewer is authorized to process, and handle generated outputs according to the organization's hiring-data policies.

Risk: Risk labels may influence hiring decisions beyond their screening purpose.

Mitigation: Treat the output as screening assistance and require human review before taking candidate-facing or employment decisions.

Risk: Resume text can include prompt-injection attempts or non-resume content.

Mitigation: Preserve the skill's injection and invalid-input checks, and review blocked or invalid cases instead of forcing a risk assessment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown report followed by a JSON code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate name/contact extraction when present, risk level, role classification, flags, usability status, and background-check focus arrays.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
