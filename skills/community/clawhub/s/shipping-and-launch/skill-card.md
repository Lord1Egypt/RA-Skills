## Description:

Prepares production launches with support for pre-launch checklists, monitoring setup, staged rollout planning, and rollback planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare production launches, including checklist creation, monitoring setup, staged rollout planning, and rollback readiness. Because the release can run commands and mixes deployment guidance with broad automation claims, users should require human approval before production-impacting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or run commands in production deployment, CI/CD, cloud, credential, rollback, or release contexts.

Mitigation: Require explicit human approval, environment confirmation, and dry-run or read-only checks before any action that could affect production systems or deployment state.

Risk: The security summary reports vague generic automation claims mixed with production deployment automation.

Mitigation: Review generated launch guidance for environment-specific correctness and limit execution authority to the minimum required for the approved deployment task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/shipping-and-launch)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with checklists, command proposals, configuration steps, and structured status or result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Production-impacting command proposals should be reviewed by a human and preceded by dry-run or read-only checks where available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
