## Description:

Reviews side-effecting code changes for retry and crash-recovery safety, identifying duplicate effects while remaining read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review changes involving side effects, retries, or crash recovery and assess whether a second run could duplicate effects or corrupt state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review findings could be treated as authorization to make changes, although this skill is explicitly read-only and its linked fixing skill and shared report documentation are not included.

Mitigation: Review findings against the code and deployment context; separately review any fixing skill before authorizing changes.

## Reference(s):

- [Retry Safety on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-retry-safety)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only findings; does not apply code changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
