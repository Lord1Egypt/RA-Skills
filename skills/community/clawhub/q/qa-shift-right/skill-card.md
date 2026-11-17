## Description:

Helps QA and release teams plan post-deployment validation through canary monitoring, production alerts, user feedback, and authorized chaos testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and release teams use this skill to plan canary checks, production monitoring, alert responses, and feedback loops after deployment. It references upstream release criteria for rollout and rollback decisions rather than setting new thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional companion-skill installation command is unpinned.

Mitigation: Verify the package and source before running it; prefer a pinned version or trusted commit.

Risk: Production chaos tests or monitoring changes could disrupt live services.

Mitigation: Require organizational authorization, limit the experiment scope, and establish rollback plans before applying changes.

Risk: Collecting production user feedback or behavior data may expose personal information.

Mitigation: Confirm user authorization and privacy compliance before collecting or processing the data.

## Reference(s):

- [Right-shift validation stages](references/right-stages.md)
- [qa-shift-right on ClawHub](https://clawhub.ai/kokxi/skills/qa-shift-right)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown validation plan and monitoring tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers canary indicators, alert thresholds and responses, optional chaos experiments, and user-feedback routing; references upstream rollback criteria.]

## Skill Version(s):

1.8.0 (source: skill metadata and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
