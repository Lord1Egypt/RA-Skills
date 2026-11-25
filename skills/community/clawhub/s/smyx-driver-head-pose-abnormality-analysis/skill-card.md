## Description:

Analyzes in-cabin driver video for head-down and side-view posture and returns head-pose findings and distraction-event reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Fleet operators and developers can use the skill to review in-cabin DMS footage for prolonged head-down or side-view behavior and retrieve related analysis reports. Treat its findings as assistive alerts that do not replace driver attention or established safety procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags possible exposure of sensitive in-cabin video and identity data, including through video uploads.

Mitigation: Obtain required driver consent, confirm upload destinations and retention, restrict access to footage, and avoid uploading video unless needed for the analysis.

Risk: The security assessment notes a gap between advertised live warnings and the reported asynchronous analysis workflow; its scan was also partial.

Mitigation: Verify alert timing and behavior in the intended deployment before relying on warnings, and retain existing driver monitoring and response procedures.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-driver-head-pose-abnormality-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured head-pose findings and distraction-event reports; Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include head-pose angles, event summaries, warning types, and report links.]

## Skill Version(s):

1.0.19 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
