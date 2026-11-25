## Description:

Analyzes pet food-bowl videos to estimate feeding duration and speed, compare results with reference thresholds, and suggest slow-feeding interventions without diagnosing disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet caregivers can submit a local food-bowl video or video URL to review when a pet eats, how long feeding takes, and estimated eating speed. The report compares results with reference thresholds and offers practical slow-feeding suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags credential and identity handling, additional account and data-management features, and possible video processing beyond stated expectations. The scan was partial and did not establish malicious intent.

Mitigation: Review the security assessment before use, submit only videos and URLs you are authorized to share, and avoid exposing credentials or identity details.

Risk: A partial scan left one local reference unreviewed, so behavior tied to it was not fully assessed.

Mitigation: Review the missing reference and related behavior before relying on the skill with sensitive videos or account-linked records.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-pet-eating-speed-slow-feed-analysis)
- [Pet eating speed API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis report, JSON, Markdown, Guidance]

**Output Format:** [Structured report in JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include feeding start and end times, duration, estimated speed, threshold comparison, intervention suggestions, and report links.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
