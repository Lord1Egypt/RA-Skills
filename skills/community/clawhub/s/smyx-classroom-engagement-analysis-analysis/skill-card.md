## Description:

Analyzes classroom video to estimate group-level student emotions and engagement, identify low-engagement seat locations, and provide teachers with heatmaps and teaching suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and classroom operators can use the skill to review group-level engagement patterns and adjust lesson pacing. Its seat-level prompts should remain anonymous teaching aids, not assessments of individual students.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill suspicious and says the scan is partial, citing concerns about account and credential handling, privacy and permissions, and video processing.

Mitigation: Review those behaviors and confirm where video and results are sent before use; limit access and retention, and follow the documented school and parent consent requirements for minors.

Risk: Facial-expression estimates and seat-level engagement cues can be mistaken for reliable judgments about a student.

Mitigation: Treat results as short-term classroom discussion aids only; do not use them for student performance decisions, public rankings, or individual psychological conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-classroom-engagement-analysis-analysis)
- [Classroom engagement API and privacy constraints](references/api_doc.md)
- [API request and error details](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance, Report links]

**Output Format:** [Structured JSON analysis results, Markdown report listings, and text suggestions with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include class-level engagement scores, estimated emotion distributions, anonymous seat coordinates, heatmaps, and teaching suggestions.]

## Skill Version(s):

1.0.17 (source: server-resolved release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
