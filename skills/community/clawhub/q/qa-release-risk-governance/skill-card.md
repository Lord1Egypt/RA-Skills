## Description:

Assesses release readiness and change risk, then recommends canary rollout, rollback, and production monitoring plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Release managers, QA teams, and developers use this skill to evaluate change and business risks, recommend release decisions, and plan staged rollout, rollback, and monitoring before production deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional command to install the broader skill set is unpinned.

Mitigation: Review the source and use a pinned, trusted version before running the install command.

Risk: Release or rollback recommendations could be mistaken for authorization to act in production.

Mitigation: Require normal production approvals and confirm rollout scope, monitoring thresholds, and rollback readiness before execution.

## Reference(s):

- [Canary rollout and rollback strategy](references/canary-rollout.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown release-risk assessment and canary rollout plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each assessment carries a REL-XXXX identifier and includes a release recommendation, risk summary, blockers, rollback plan, and monitoring recommendations.]

## Skill Version(s):

1.8.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
