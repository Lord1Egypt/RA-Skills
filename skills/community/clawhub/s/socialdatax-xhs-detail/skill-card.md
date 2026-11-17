## Description:

Retrieves structured details and engagement metrics for Xiaohongshu (XHS/RedNote) notes through SocialDataX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve structured details for a Xiaohongshu note, including available content and engagement metrics, for content research and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI resolves a mutable package release, creating supply-chain risk around local permissions and credentials.

Mitigation: Review the resolved package before running it, use a least-privilege environment, and keep credentials in the documented private credential store or existing secret injection.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-detail)
- [SocialDataX API access and key management](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON note details with factual text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only detail data; fields depend on the source response.]

## Skill Version(s):

0.1.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
