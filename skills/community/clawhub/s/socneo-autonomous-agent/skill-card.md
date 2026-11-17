## Description:

AI autonomous agent framework that implements perception, judgment, execution, and reflection layers for self-aware, adaptive operation with safety and user-control concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socneo](https://clawhub.ai/user/socneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a framework for autonomous monitoring, task evaluation, execution resilience, reflection, and adaptive learning workflows. It is most appropriate for tightly scoped agent experiments or assisted automation where human oversight remains available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous monitoring and safety claims are not fully proven by the provided implementation.

Mitigation: Use assisted mode, keep human review in the loop, and validate permission, override, audit, and rollback behavior in a controlled environment before enabling autonomous operation.

Risk: Artifact behavior includes filesystem monitoring and log/config inspection paths that may exceed the intended scope.

Mitigation: Run with an explicit filesystem allowlist, disable broad log scanning where possible, and execute under a sandbox or read-only permissions until scope is verified.

Risk: Recovery and permission behavior includes simulated or under-scoped controls, including elevated-permission and rollback paths.

Mitigation: Do not rely on claimed rollback or elevated-permission safeguards without implementation review, tests, and environment-specific authorization checks.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/socneo/skills/socneo-autonomous-agent)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown instructions with Python modules and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes autonomous monitoring, risk assessment, recovery, progress tracking, reflection, and memory components; review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
