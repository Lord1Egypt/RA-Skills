## Description:

Analyzes bathroom occupancy monitoring media to flag stays exceeding 30 minutes and provide alerts and reports for caregivers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and elder-care teams use this skill to review bathroom occupancy alerts and historical reports from video monitoring. Alerts are prompts for a human check, not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bathroom-monitoring media and report history are highly sensitive and processed by configured cloud services.

Mitigation: Obtain the monitored person's informed consent, minimize captured details, and review cloud data handling before use.

Risk: A hidden identity override, silent account creation, and locally persisted tokens or profiles may expose or misassociate reports.

Mitigation: Review or remove the identity override and automatic account creation; protect or disable local credential and profile persistence before using real care data.

Risk: Occupancy alerts may be inaccurate and are not medical diagnoses.

Mitigation: Have a caregiver promptly verify urgent alerts by phone or in person rather than relying on the skill alone.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/18072937735/skills/smyx-elderly-toilet-time-abnormal-analysis)
- [Bathroom monitoring API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Alerts, Reports]

**Output Format:** [Text, JSON, or Markdown tables with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save results to a local file or retrieve historical reports.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata; bundled frontmatter says 1.0.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
