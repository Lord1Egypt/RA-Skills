## Description:

Analyzes supplied facial video for micro-expression and emotion cues and returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Users can submit facial video for an AI-generated micro-expression and emotion report or request a list of saved reports. Results are advisory and depend on the quality of the supplied video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious because account, identity, credential, and facial-media handling is not adequately explained; its summary also says some behavior may occur when analysis is disabled.

Mitigation: Before use, verify why registration and identity or token storage are needed, and confirm when facial media and identity data are sent, retained, or accessed. Treat the current scan as partial because a referenced path was missing.

## Reference(s):

- [API interface notes](artifact/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured emotion-analysis report with findings, advisory suggestions, and report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output; video quality affects results, and the analysis does not replace professional psychological assessment.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
