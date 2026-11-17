## Description:

Analyzes nighttime bedroom or hallway footage for older adults' bed exits and wandering, then provides activity summaries and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and developers in home or residential elder care use the skill to analyze nighttime video for prolonged bed exits or wandering and review alerts and historical reports. Alerts support, but do not replace, human assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private bedroom footage and report queries are processed by a cloud service.

Mitigation: Obtain informed consent from the monitored person or legal caregiver; confirm the service's access, location, and retention policies before use.

Risk: The skill silently creates or reuses local identities and tokens for cloud access.

Mitigation: Review who controls the service account, where tokens are stored, and whether stricter confirmation or on-premise processing is needed.

Risk: Automated alerts may be inadequate for urgent care decisions.

Mitigation: Have caregivers verify suspected falls or missing persons promptly and follow established emergency procedures.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-elderly-night-bed-exit-wandering-analysis)
- [Analysis API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text analysis summaries and alerts; Markdown tables for historical reports, with optional saved report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bed-exit duration, wandering indicators, alert levels, and report links.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
