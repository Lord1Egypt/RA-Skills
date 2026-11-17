## Description:

Based on facial video, identifies abnormal rhythms such as premature beats, atrial fibrillation, tachycardia/bradycardia, assists in early detection of heart health risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals or care teams can submit facial video for an early warning screen for possible rhythm abnormalities and retrieve prior reports. The results are for risk screening and do not replace ECG testing or a clinician's diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identifiable facial videos may be uploaded; the export-only option still permits uploads, and account creation and credential storage controls are unclear.

Mitigation: Wait for a working export-only option and clearer privacy and account controls before sharing identifiable video. Confirm report access, video and credential retention or deletion, and any service charges.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-arrhythmia-early-warning-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API interface documentation](references/api_doc.md)
- [API reference and error codes](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis reports and Markdown tables for report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes screening results, recommendations, and report links; results do not replace ECG testing or clinician diagnosis.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
