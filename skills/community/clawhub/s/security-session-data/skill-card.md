## Description:

Security engineer skill for session configuration, area isolation, sensitive-state handling, and data-protection boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review session configuration, auth-area separation, sensitive-state handling, and session-backed data protection. It helps preserve frontend, backend, and request-boundary isolation while documenting validation evidence and residual risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session or sensitive request state could leak across frontend, backend, or request boundaries if changes are applied without exercising the real auth flow.

Mitigation: Validate login, logout, protected-path behavior, and state isolation across affected areas, then record any residual retention or migration risk.

Risk: Direct raw session manipulation could bypass the framework isolation model.

Mitigation: Use framework session factories, area config, and controlled config paths instead of direct global session access.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code, shell command, and configuration recommendations when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation evidence, residual-risk notes, and collaboration status for high-risk session or data-protection changes.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
