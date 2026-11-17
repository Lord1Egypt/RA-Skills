## Description:

Identifies known people in images or videos by comparing faces against an enrolled database and returns recognition results with locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Home and office security users can compare people in images or videos with an enrolled acquaintance database and review matches, locations, and analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facial images may be sent to a remote analysis service, and identity information may be linked to accounts or reports.

Mitigation: Use only with appropriate consent and authorization; review the service's data handling and access to account-linked reports before submitting images.

Risk: The export-only option may not prevent analysis from running.

Mitigation: Do not rely on export-only mode to avoid processing; confirm the intended action before invoking the skill and submit only data you are authorized to process.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-familiar-person-recognition-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [JSON analysis results and Markdown report listings, with report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recognized identities, locations, and report links.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
