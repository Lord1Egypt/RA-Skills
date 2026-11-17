## Description:

Analyzes a submitted study-area video to estimate a child's posture, produce reminder text, and return structured posture reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, educators, and teams integrating smart study desks can submit a child's study-area video for estimated posture metrics, reminder text, and a session report, or request previously generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A child's study-area video may be uploaded to a remote service, and the scanner flags privacy concerns.

Mitigation: Obtain a guardian's informed consent and review the service's video handling before submitting footage; limit video to what is needed for posture review.

Risk: The scanner flags identity and token handling concerns.

Mitigation: Review credential handling and access controls before use, and keep any API credentials out of user-visible output.

Risk: The scanner found a mismatch between advertised real-time reminders and the submitted-video analysis and report-history behavior it observed.

Mitigation: Confirm the desired workflow and capabilities with a non-sensitive sample before relying on it for live monitoring.

Risk: Visual posture and Cobb-angle estimates could be mistaken for medical assessment.

Mitigation: Present results only as posture guidance; do not use them for diagnosis or as a substitute for professional medical evaluation.

## Reference(s):

- [Posture analysis API reference](references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-child-poor-posture-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured posture analysis and report data; history results may be presented as a Markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posture and Cobb-angle values are visual estimates, not medical diagnoses; the skill documentation says they do not replace medical evaluation.]

## Skill Version(s):

1.0.18 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
