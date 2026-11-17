## Description:

Analyzes video of a child's study area to estimate per-minute focus, identify distraction periods, and produce focus reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and teachers use the skill to review a child's study-session video, see estimated focus scores and distraction periods, and follow changes in study behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags remote processing of children's videos and unclear handling of identity or credential data.

Mitigation: Before use, clarify where footage and identity data are sent, what is stored, and who can access it; obtain explicit guardian consent and limit uploads to authorized footage.

Risk: The security guidance reports an HTTP configuration risk.

Mitigation: Use HTTPS endpoints where available and avoid sending sensitive video or identity data over unencrypted connections.

Risk: The security scan was partial because a referenced local path was missing, so not every relevant component was assessed.

Mitigation: Review the missing component and complete a full security assessment before relying on the scan.

Risk: The security summary reports unclear purpose alignment and broad activation.

Mitigation: Review the skill's triggers and intended scope before enabling it, and restrict activation to the study-video analysis tasks you intend to support.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-focus-analysis-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured focus report with per-minute scores and distraction event summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an overall focus level, distraction duration, alerts, and a report link when returned by the service.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
