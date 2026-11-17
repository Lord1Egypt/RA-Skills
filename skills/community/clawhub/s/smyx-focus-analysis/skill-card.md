## Description:

Real-time detection of gaze direction and facial pose to quantify focus, distraction, and mind-wandering in classroom, office, and driving videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, meeting facilitators, and fleet safety teams can use the skill to review video for gaze direction, head pose, estimated focus and distraction patterns, and attention trends. Treat results as advisory and combine them with human assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says account and token handling is not clearly explained.

Mitigation: Before use, clarify how identities and credentials are created, stored, associated with requests, and protected.

Risk: The security assessment flags potentially unexpected uploads of video to a remote service.

Mitigation: Confirm remote processing and retention practices, and submit recordings only when you are authorized to do so.

Risk: The security assessment warns that a shared default identity could expose another sender's reports.

Mitigation: Use isolated per-user identities and confirm report access is properly separated before querying history.

## Reference(s):

- [Skill introduction](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Report links]

**Output Format:** [Structured analysis reports in JSON or Markdown, with optional report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scene, analysis duration, focus threshold, and detail level are configurable; results can optionally be saved to a file.]

## Skill Version(s):

1.0.20 (source: server-resolved release record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
