## Description:

Analyzes a supplied aquatic pet video and returns a structured health report with observations, potential concerns, and care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium owners can submit a local video or video URL for a structured assessment of visible features such as scales, fins, coloration, and activity. The report is informational and does not replace veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious over unexpected account and profile handling, report history lookups, and remote media processing or uploads, including with an export-only option. The scan was partial and one referenced item was missing.

Mitigation: Review the behavior before installation. Until the unexpected flows are understood, avoid sending sensitive videos or using account and history features.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-aquarium-analysis)
- [Aquatic health analysis API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured health report in text, Markdown, or JSON, with report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observations, potential health concerns, and care suggestions; results are informational and not a veterinary diagnosis.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
