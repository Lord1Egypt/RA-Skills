## Description:

Analyzes thermal-camera imagery of a group, compares each person's estimated skin-surface temperature with the group average, and reports relative anomalies for follow-up measurement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Households and operators of group settings can use this skill to screen thermal-camera footage for people whose measured skin-surface temperature differs from the group average, then arrange a follow-up measurement with a calibrated thermometer. It provides directional screening alerts rather than a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unclear account and credential handling, external data transmission, and video analysis that may occur despite an export-only option; the scan was partial and does not establish intent.

Mitigation: Avoid installation until account handling, credential transmission, and video processing are clearly explained and the export-only behavior is corrected; review the partial scan before use.

Risk: Thermal video and related health screening reports may contain sensitive personal information.

Mitigation: Obtain participants' informed consent and protect video and reports with appropriate access controls and encryption.

## Reference(s):

- [Thermal Screening API Reference](references/api_doc.md)
- [Skill Demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Recommendations]

**Output Format:** [Structured analysis results and report summaries with alert text and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports relative temperature differences and suggests follow-up measurement; it does not provide a medical diagnosis.]

## Skill Version(s):

1.0.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
