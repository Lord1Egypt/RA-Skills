## Description:

Analyzes short adult facial videos for heart-rate variability (HRV) metrics and trends using remote photoplethysmography (rPPG), and retrieves prior reports from the cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Adults and health-monitoring teams use this skill to review HRV metrics and trends from short facial videos, including previous cloud reports. Results are wellness trends, not medical diagnoses or clinical cardiovascular assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facial video and HRV-related data are processed by the Life Emergence cloud service.

Mitigation: Obtain explicit consent and confirm cloud data retention and deletion terms before analysis.

Risk: The skill silently creates or reuses a local identity and stores authentication tokens in SQLite.

Mitigation: Review access to the local identity and token store, and protect the workspace from unauthorized access.

Risk: Historical cloud report queries are tied to that identity and may be triggered by report requests.

Mitigation: Confirm with the user before retrieving historical reports from the cloud.

Risk: Short camera-based HRV measurements may be misleading if used for clinical decisions.

Mitigation: Present results as personal trends only, not a diagnosis or substitute for medical-grade assessment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-facial-hrv-trend-monitoring-analysis)
- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Structured report or JSON; Markdown table for historical reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HRV metrics, trends, signal quality, guidance, and report links.]

## Skill Version(s):

1.0.14 (source: server-resolved ClawHub release; bundled skill frontmatter says 1.0.19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
