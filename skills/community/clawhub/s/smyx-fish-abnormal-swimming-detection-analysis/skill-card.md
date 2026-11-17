## Description:

Analyzes fixed-camera aquarium video to identify abnormal fish swimming postures and report their duration relative to the observation period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarists and aquarium operators use the skill to review fixed-camera fish video, identify unusual swimming posture, and inspect an abnormal-duration summary. Its results are visual observations and do not diagnose fish disease.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious, citing account and credential handling, broad remote actions, and behavior that does not consistently match its fish-video analysis purpose.

Mitigation: Review the skill and its requested permissions before use; avoid supplying sensitive credentials or production account access until the reported behavior is understood.

Risk: The security scan is partial because a local path-like reference was missing, so it does not cover every referenced item.

Mitigation: Check that referenced files and dependencies are present and review them before installing or running the skill.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-abnormal-swimming-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Report links]

**Output Format:** [Structured posture analysis and duration metrics, with Markdown summaries and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include posture categories, abnormal-duration proportions, alerts, and recommendations.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata; artifact frontmatter says 1.0.21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
