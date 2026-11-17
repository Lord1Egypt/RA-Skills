## Description:

Analyzes resting older adults' bedroom videos to estimate breathing rate and flag elevated rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and care-platform operators use this skill to review resting breathing patterns from bedroom video and retrieve prior screening reports. Results are alerts for follow-up, not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive bedroom footage or video URLs are sent to configured cloud services.

Mitigation: Obtain consent from the monitored person or caregiver and review the service destination before submitting footage.

Risk: The skill automatically creates or reuses locally stored identity tokens.

Mitigation: Review access to the workspace data database and clear stored tokens when the skill is no longer used.

Risk: Breathing-rate alerts could be mistaken for medical diagnoses.

Mitigation: Treat results as non-diagnostic screening and seek qualified medical assessment for concerning symptoms.

## Reference(s):

- [Skill API documentation](references/api_doc.md)
- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-elderly-tachypnea-detection-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Text or JSON-formatted analysis reports; Markdown tables for report history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes breathing-rate estimates, risk alerts and report links; reports can be saved to a file.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
