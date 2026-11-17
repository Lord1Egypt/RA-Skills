## Description:

Analyzes UAV orthomosaics or RGB and multispectral imagery to calculate vegetation indices and produce a crop-health heatmap with flagged zones and a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Farm operators, agricultural cooperatives, and UAV crop-monitoring services can use this skill to review crop vigor from aerial imagery and locate areas for field inspection. Results are index-based assessments and should be checked against field conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags unresolved account and identity handling, credential behavior, remote destinations, upload disclosures, and an export-only mode that may still run analysis.

Mitigation: Do not install until these behaviors and disclosures are clarified and the export-only mode is fixed; avoid submitting sensitive imagery until remote handling is understood.

## Reference(s):

- [API interface and supported indices](references/api_doc.md)
- [Skill introduction video](https://lifeemergence.com/sample.html)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-uav-farm-health-index-map-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [Structured JSON or Markdown report with heatmap and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vegetation-index statistics, flagged-zone coordinates and area estimates; verify findings in the field.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
