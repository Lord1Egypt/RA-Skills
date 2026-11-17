## Description:

Analyzes fixed-camera video from emergency shelters for visible behavior associated with acute stress and returns alerts for review by on-site psychological rescue teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized emergency command centers and licensed psychological rescue teams can use this skill to review fixed-camera shelter video for visible stress-related behavior and prioritize in-person checks. It provides behavioral observations and response suggestions, not clinical diagnoses.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive shelter video may be uploaded for external processing; identity and credential handling, including credentials sent to caller-selected destinations, is also reported as a concern.

Mitigation: Use only an authorized emergency-response deployment, confirm service destinations and access controls, restrict footage to rescue use, and delete raw video within seven days.

Risk: The security scan is partial and reports concerns that are not clearly justified by the stated analysis purpose; it does not establish the skill's full behavior or malicious intent.

Mitigation: Review the deployment and data flow before use. Treat alerts as behavioral observations, and require licensed responders to verify high-risk findings before dispatch; do not use them as diagnoses.

## Reference(s):

- [API interface documentation](artifact/references/api_doc.md)
- [Skill introduction demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Guidance]

**Output Format:** [Structured behavioral analysis reports with alerts, location cues, response suggestions, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Observational alerts require human review and are not clinical diagnoses.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
