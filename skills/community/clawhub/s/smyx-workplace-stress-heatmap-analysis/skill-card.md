## Description:

Analyzes fixed-camera footage from workplace areas to estimate zone-level stress signals and produce a workplace heatmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Workplace health, facilities, and operations teams can use the skill to summarize office camera footage into area-level stress indicators and heatmaps for organizational monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags workplace video being sent to a remote service, while the destination and handling are unclear.

Mitigation: Avoid installing or sending footage until the publisher explains the destination, retention, access, and processing of video.

Risk: The assessment flags account and credential processing beyond the stated anonymous analysis; partial coverage does not establish whether identities are linked to analysis.

Mitigation: Require an explanation of account and credential use, and review the complete behavior before providing credentials.

Risk: The export-only behavior and some imported behavior could not be verified because scanner coverage was partial and a referenced local path was missing.

Mitigation: Resolve the missing path and review the export flow before use; treat unverified behavior as unresolved.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-workplace-stress-heatmap-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Structured JSON analysis results; historical report lists can be presented as Markdown, with report and heatmap links when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zone-level indicators, stress scores, trends, alerts, and management suggestions.]

## Skill Version(s):

1.0.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
