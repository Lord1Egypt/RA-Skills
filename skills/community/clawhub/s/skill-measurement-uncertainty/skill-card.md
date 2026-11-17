## Description:

Helps laboratory and metrology engineers assess measurement uncertainty using the GUM method, combine Type A and Type B uncertainty components, and produce structured uncertainty reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

External laboratory, calibration, quality, and metrology teams use this skill to collect measurement data, classify uncertainty contributors, calculate combined and expanded uncertainty, and draft reports for human review. It is an aid for measurement-uncertainty assessment and does not replace accredited calibration or testing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could treat the generated report as an accredited calibration or testing decision.

Mitigation: Require review and approval by authorized laboratory or metrology personnel before relying on the report.

Risk: Referenced helper scripts and reference files are not included in the inspected artifact, so automated report generation may be unavailable or incomplete.

Mitigation: Confirm the available tooling and calculations in the deployment environment, or generate and verify the report manually.

Risk: Missing measurement data, calibration certificate uncertainty, distribution assumptions, or coverage factors can make the uncertainty result misleading.

Mitigation: Do not invent missing values; keep them marked as required enterprise inputs and explain their impact on the combined uncertainty.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-measurement-uncertainty)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-measurement-uncertainty)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown and HTML report drafts with uncertainty component tables, calculations, and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve missing enterprise inputs as items to be supplied and should be reviewed by authorized metrology personnel.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
