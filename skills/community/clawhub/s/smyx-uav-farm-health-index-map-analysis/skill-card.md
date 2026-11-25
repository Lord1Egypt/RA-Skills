## Description:

Analyzes UAV farmland imagery to estimate vegetation indices and produce crop health maps and structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Farm operators and agricultural analysts use the skill to review UAV imagery and receive vegetation-index summaries, health maps, and flagged areas. Results are screening information for field review, not specific treatment instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security assessment rates this release suspicious and reports credential exposure and persistence risks, remote account creation, possible media uploads without clear disclosure, and possible analysis when using the export-only option; its review is partial.

Mitigation: Review the source and behavior before installation. Use an isolated environment without sensitive credentials or imagery, check upload destinations and outbound access, and verify export-only behavior before relying on it.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-uav-farm-health-index-map-analysis)

## Skill Output:

**Output Type(s):** [Analysis results, JSON reports, Markdown reports, Map and report links]

**Output Format:** [Structured JSON and concise text; Markdown tables for report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health maps, index summaries, and flagged-area coordinates or area estimates when returned by the analysis service; use results as screening information and verify in the field.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
