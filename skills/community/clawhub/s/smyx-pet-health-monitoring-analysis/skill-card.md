## Description:

Analyzes pet monitoring videos for behavior patterns and potential health changes, then returns a structured monitoring report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and care teams use the skill to review monitoring videos for eating, drinking, elimination, activity, vomiting, or limping patterns and view health monitoring reports. Its results are for reference and do not replace veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unclear account and token handling.

Mitigation: Clarify how account information and tokens are handled before use.

Risk: Monitoring footage may be transmitted to an external service.

Mitigation: Confirm what footage and related data are sent, where they go, and whether that transfer is acceptable before providing video.

Risk: Analysis may run even when an export-only option is selected.

Mitigation: Confirm whether analysis runs in export-only mode before relying on that option.

Risk: The security review is incomplete because a referenced local path was missing.

Mitigation: Review the full skill behavior, including the missing reference, before installation or use.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Analysis API details](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-health-monitoring-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured health monitoring report with behavior findings, warnings, care suggestions, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For health reference only; not a veterinary diagnosis.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
