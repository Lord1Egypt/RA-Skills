## Description:

Analyzes infant sleep videos for prone positioning, head covering, and possible mouth or nose occlusion, then returns a risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers or operators can submit an infant sleep video for an on-demand review of sleep position and possible facial covering, receive a structured report, or query prior cloud reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised real-time infant-safety alerts are not substantiated by the reported on-demand video analysis.

Mitigation: Do not rely on this skill for real-time monitoring or as a substitute for adult supervision; respond directly to any observed risk.

Risk: Video upload, account registration, credential handling, and report export behavior have unresolved privacy and handling concerns.

Mitigation: Avoid installation and uploading identifiable footage until those behaviors are clarified and addressed; do not provide credentials through the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-infant-suffocation-warning-analysis)
- [Usage demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a local video file or video URL; sensitivity can be set from 1 to 5; supports cloud history lookup. Reports are supplemental and do not replace adult supervision.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
