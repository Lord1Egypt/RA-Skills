## Description:

Analyzes sleep-monitoring videos to estimate sleep stages, body movement, nighttime awakenings, and possible sleep-apnea indicators, then returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

People using sleep-monitoring cameras can review estimated sleep stages, movement, awakenings, and respiratory indicators from a video, then retrieve prior analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags transfer of sensitive sleep recordings to a remote service.

Mitigation: Review and approve the destination and data handling before sending personal recordings; use a non-sensitive sample until reviewed.

Risk: The security assessment flags account registration and credential handling as insufficiently disclosed.

Mitigation: Review the account and token handling paths before enabling the skill or providing credentials.

Risk: The security assessment flags report-query triggers and behavior that may exceed or mismatch the stated purpose.

Mitigation: Review the automatic report-query triggers and require explicit authorization before accessing cloud-hosted report history.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-sleep-quality-analysis)
- [API reference](artifact/skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Text]

**Output Format:** [Structured sleep-analysis report; report history is presented as a Markdown table with links when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include sleep-stage, movement, awakening, and respiratory indicators. Results are for reference and do not replace professional sleep monitoring or medical diagnosis.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
