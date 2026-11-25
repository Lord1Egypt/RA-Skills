## Description:

Uses a fixed home camera to estimate prolonged standing, bending, and related posture for a pregnant woman, track activity duration and frequency, and provide fatigue reminders for health reference rather than medical diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Expecting parents, prenatal educators, and community health teams can use the skill to review fixed-camera video for posture and activity patterns and receive gentle rest reminders. Its estimates are for general health reference and do not replace medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera footage of a pregnant person is sensitive, and the security assessment reports that shared-account behavior could expose analysis history across senders.

Mitigation: Obtain the subject's informed consent, restrict access to footage and reports, and use the skill only where account separation is understood and appropriate.

Risk: The security assessment reports that an export-only option may still trigger video analysis unexpectedly.

Mitigation: Review the requested operation and input before running it, and avoid invoking export-related actions until their behavior is confirmed.

Risk: The security assessment is suspicious and incomplete: one component was partially inspected and the tool-misuse analyzer was degraded.

Mitigation: Review the skill and its security findings before installation or use, and treat its behavior as not fully assessed.

## Reference(s):

- [Skill API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pregnant-posture-fatigue-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured posture and activity summary with fatigue reminders and report links; JSON detail is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on clear full-body camera footage; results are health reference only, not a diagnosis.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
