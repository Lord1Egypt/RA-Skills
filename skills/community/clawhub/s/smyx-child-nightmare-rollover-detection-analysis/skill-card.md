## Description:

Analyzes submitted child sleep recordings for movement, crying, and sleep talk, then produces sleep-behavior summaries and possible restlessness or nightmare alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers can review a child's submitted night-time audio and video for movement, crying, sleep talk, and other sleep behaviors. The reports are an aid to caregiving and are not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected child recordings may still be uploaded when the no-analysis option is used.

Mitigation: Do not submit recordings until the publisher fixes this behavior. Obtain informed guardian consent before any use that sends recordings to LifeEmergence.

Risk: Automatic account handling has unclear user control, and remote registration, credential handling, account separation, and recording retention or deletion need clarification.

Mitigation: Wait for the publisher to document and address these account and recording controls before use.

Risk: The skill should not be relied on for continuous monitoring or for delivery of parental alerts.

Mitigation: Treat its results as an occasional review aid and do not rely on it for supervision or time-critical alerts.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-nightmare-rollover-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis results; Markdown for report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes sleep events and estimated sleep quality, with possible restlessness or nightmare flags and report links; not a medical diagnosis.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
