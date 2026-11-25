## Description:

Detects and analyzes indoor plant light stress from images and optional lux data, identifies signs of insufficient or excessive light, and suggests adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Indoor plant owners and home or office gardeners use the skill to assess possible low- or excessive-light stress from plant images, optionally with lux readings, and receive care suggestions or query prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious due to privacy disclosure gaps, unintended analysis and data handling risks, and questionable credential and workspace boundaries. The scan was partial (28 of 29 components) and included a malformed manifest and unresolved reference.

Mitigation: Do not install until the developer clarifies when images are uploaded, explains API credential and local data handling, fixes the export-only behavior, and completes the scan.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-indoor-plant-light-stress-detect-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Text analysis report with structured JSON content; Markdown table for history lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a report link; analysis results can be saved to a file.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
