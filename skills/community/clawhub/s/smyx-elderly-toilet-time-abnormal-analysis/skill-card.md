## Description:

Analyzes privacy-conscious bathroom doorway video to track an older adult’s entry and exit, measure occupancy, and flag stays beyond a configurable threshold (30 minutes by default).

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and operators of senior living settings use the skill to review doorway or silhouette-only video, track toilet occupancy, and receive an alert when a stay exceeds the configured threshold. It supports human follow-up and does not provide medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, citing undeclared account and identity handling, possible exposure of sensitive video, and a mismatch between the stated monitoring purpose and observed behavior.

Mitigation: Consider avoiding installation unless the external video-processing service and its privacy protections can be verified; understand what identity and account data may be sent or stored; and confirm export-only mode prevents analysis. The scan is partial and does not establish all downstream behavior.

## Reference(s):

- [API interface and output fields](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-elderly-toilet-time-abnormal-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Alerts, Structured reports, JSON, Markdown]

**Output Format:** [Structured analysis text or JSON, with report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Threshold-based occupancy alerts and history reports; does not provide medical diagnoses.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
