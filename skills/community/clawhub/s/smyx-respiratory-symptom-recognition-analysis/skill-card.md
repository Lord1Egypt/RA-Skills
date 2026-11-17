## Description:

Analyzes video to detect and count coughing, phlegm, and wheezing episodes and produce respiratory health monitoring reports for early alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers can review respiratory symptom counts from a video and retrieve prior monitoring reports. Treat results as early monitoring information and consult a clinician for diagnosis or urgent symptoms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags account, credential, and network behavior as broader than the stated respiratory analysis purpose; the assessment is partial.

Mitigation: Review the actual account and credential handling and remote video processing before installation; avoid sending sensitive health videos until you are comfortable with the service.

Risk: Video-based symptom estimates could be mistaken for a medical diagnosis.

Mitigation: Use reports only as monitoring aids, consult a clinician for diagnosis, and seek urgent care for serious breathing difficulty.

## Reference(s):

- [Respiratory symptom analysis API documentation](references/api_doc.md)
- [Skill usage introduction](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-respiratory-symptom-recognition-analysis)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text, Guidance]

**Output Format:** [Structured JSON analysis results and Markdown report lists, with health alerts and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts local video files or public video URLs and supports history lookup; video requirements are MP4, AVI, or MOV up to 10 MB.]

## Skill Version(s):

1.0.23 (source: server-resolved release metadata; SKILL.md frontmatter says 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
