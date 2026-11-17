## Description:

Looks up a TikTok creator's published videos by user ID or unique ID using Qinghu's data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and commerce analysts use this skill to review a TikTok creator's recent videos and assess content performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the external qhkit CLI requires a Qinghu API token.

Mitigation: Review or pin the package version in controlled environments and configure the token only when needed.

Risk: Video lookups may consume paid Qinghu credits, especially for larger result sets.

Mitigation: Estimate the cost and obtain user approval before paid calls; disclose actual credit usage afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-creator-videos)
- [Qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise prose with an optional Markdown preview or tabular export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports paid-call credit usage; larger result sets may be delivered as a file.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
