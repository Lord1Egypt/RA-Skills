## Description:

Analyzes rehabilitation training video and optional audio for signs of frustration or disengagement and provides structured findings and encouragement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Rehabilitation clinicians and authorized caregivers use the skill to assess training-session recordings for possible frustration or disengagement, review progress-based encouragement suggestions, and identify when human support may be needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive rehabilitation video or audio may be processed in the cloud and linked to patient identities.

Mitigation: Obtain explicit patient or authorized caregiver consent before use and confirm which cloud services receive the media and identity data.

Risk: Patient history, report links, and access tokens may be retained or exposed beyond the intended audience.

Mitigation: Verify the service's retention policy, token storage location, report access controls, and authorized alert recipients before deployment.

Risk: Automatic escalation may notify therapists or family members without human review.

Mitigation: Confirm whether escalation can be disabled or require human approval, and review alert recipients and thresholds before enabling it.

## Reference(s):

- [Rehabilitation motivation API documentation](references/api_doc.md)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-rehab-motivation-encouragement-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured report or JSON; Markdown table for historical reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include findings, encouragement suggestions, historical report links, and escalation recommendations.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
