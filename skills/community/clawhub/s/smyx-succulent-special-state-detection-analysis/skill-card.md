## Description:

Analyzes succulent images and video to identify black rot, translucent water-soaked leaves, and stretching, then reports the detected condition, severity, confidence, and affected area.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Succulent owners, greenhouse operators, and florists can submit plant images or video to review signs of black rot, water-soaked leaves, or stretching, and check prior analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags image uploads and remote analysis as insufficiently disclosed.

Mitigation: Submit only images you are authorized to share, and confirm the service's data handling before uploading.

Risk: The security review flags account creation and credential handling as undeclared.

Mitigation: Review and authorize the account and credential behavior before use; do not expose credentials you are not permitted to share.

Risk: The security review warns that export-only mode may still start analysis.

Mitigation: Do not assume export-only avoids analysis; verify its behavior before using it with sensitive media.

Risk: The security scan was partial because a referenced local path was missing, so its results are incomplete.

Mitigation: Review the missing path and complete the package scan before relying on the scan results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-succulent-special-state-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API interface documentation](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis results; Markdown tables for report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports condition, severity, confidence, and affected area; report listings include links when available.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
