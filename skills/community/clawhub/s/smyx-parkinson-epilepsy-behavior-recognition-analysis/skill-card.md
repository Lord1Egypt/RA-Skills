## Description:

Analyzes images and videos for tremors, convulsions, stiffness, and gait abnormalities to support home monitoring of people with chronic conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and developers use the skill to review monitoring images or videos for possible abnormal movements and retrieve cloud-hosted analysis reports. Results support monitoring, not medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patient or bystander media and linked identity data are sent to an external service without clear user-facing consent.

Mitigation: Review the service and consent model; upload only media that users are authorized to share.

Risk: Persistent accounts, stored tokens, and cloud reports may retain sensitive information without clear deletion controls.

Mitigation: Confirm identity linkage, token handling, retention, and deletion or reset processes before use.

Risk: Behavior-recognition results could be mistaken for a clinical diagnosis.

Mitigation: Use results only for monitoring support and seek qualified medical judgment for clinical decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-parkinson-epilepsy-behavior-recognition-analysis)
- [Analysis API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with structured analysis results and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list past reports or save analysis to a file; local uploads are limited to 10 MB. Not a medical diagnosis.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata; bundled SKILL.md lists 1.0.20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
