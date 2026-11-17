## Description:

Analyzes multi-day bedroom and dining-area camera footage for changes in time in bed and eating behavior, and produces reports for caregiver follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family caregivers and community care staff can review multi-day changes in an older or solo-living person's time in bed and eating behavior. The report is an observational prompt for follow-up, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bedroom and dining-area footage can reveal highly sensitive personal and health-related information.

Mitigation: Obtain the subject's informed consent, enable silhouette and face masking, and retain anonymized metrics instead of raw video.

Risk: The security review rates this skill suspicious and flags possible undisclosed account or credential handling and behavior outside its stated analysis purpose.

Mitigation: Review account and credential handling and confirm where footage and results are sent before use; limit credentials and access to what the task requires.

Risk: Behavioral changes alone cannot establish depression or another diagnosis.

Mitigation: Use reports to prompt follow-up with family or a qualified clinician, and seek urgent local help for self-harm concerns.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-depression-behavioral-markers-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API interface documentation](artifact/references/api_doc.md)
- [Analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON results and Markdown summaries or reports with optional report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes continuous 24-hour-or-longer footage covering bedroom and dining areas; comparison uses a 7–14-day personal baseline when available.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
