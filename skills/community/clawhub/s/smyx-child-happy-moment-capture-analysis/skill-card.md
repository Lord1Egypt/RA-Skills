## Description:

Analyzes video from fixed cameras to identify children's positive expressions and behavior, capture selected moments, and create reports for caregivers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and childcare providers use the skill to review video for children's positive moments and receive event summaries or historical report links. Public settings require appropriate consent for children's images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because its child happiness purpose is paired with account, identity, and video-analysis capabilities; video and identity data flows, credentials, and user records need review.

Mitigation: Before use, verify where video and identity data go, how credentials and user records are handled, and what access and retention controls apply. Use only after reviewing and accepting those data flows.

Risk: It is unclear whether the export-only option can trigger analysis.

Mitigation: Confirm its behavior before use, and do not rely on it to avoid processing sensitive footage until verified.

Risk: The security assessment had partial coverage and did not verify referenced material.

Mitigation: Review referenced material and the complete package before installation or use.

## Reference(s):

- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured analysis reports with event results and report links; Markdown tables for historical report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected positive events, recommendations, and links to saved reports.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
