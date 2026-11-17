## Description:

Analyzes a child's facial video for eye closure, head nodding, and related visual cues to estimate drowsiness and produce a fatigue score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and educators can use the skill to review a child's study-session video for visual signs of drowsiness, receive a fatigue estimate and rest reminder, or retrieve prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis may involve remote processing of a child's facial video, which is sensitive personal data.

Mitigation: Obtain the guardian's informed consent before use, and confirm where video is sent and how reports are retained.

Risk: The security assessment flags account and credential handling and says an environment-only option may not reliably prevent analysis.

Mitigation: Review the account and credential access before running the skill, and confirm whether analysis will execute; do not rely on the environment-only option as a safety control.

Risk: Security coverage is partial, so the artifact's complete behavior has not been established.

Mitigation: Review the full package and its data flows before use with children's video.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-drowsiness-fatigue-detection-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured fatigue analysis results and Markdown report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual fatigue estimates and directional rest reminders; not a medical diagnosis.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
