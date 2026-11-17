## Description:

Analyzes monitoring images or videos to identify possible personnel absences from assigned posts and returns a structured monitoring report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and site managers use this skill to review images or video from staffed areas such as production floors, control rooms, and service counters. It estimates on-duty status and absence durations and produces a report for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious because of credential and account handling, video uploads, and report-history access; the scan is incomplete because a local reference was missing.

Mitigation: Before installing, review account registration, local token storage, video uploads, and report-history access against your privacy and security requirements.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [Structured JSON or human-readable monitoring report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post status, absence counts and durations, detection time, recommendations, and report links; results can be saved to a file.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
