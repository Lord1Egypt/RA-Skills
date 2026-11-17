## Description:

Manage Volcengine ECS instances and related resources for inventory, lifecycle operations, troubleshooting, and automation templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and cloud operators use this skill to inspect Volcengine ECS inventory, prepare scoped lifecycle actions, troubleshoot instances, and draft automation-oriented operational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud operations could affect unintended Volcengine ECS resources if account scope, region, filters, or target instance IDs are ambiguous.

Mitigation: Confirm account scope, region, filters, and explicit target IDs before lifecycle actions; query inventory before mutating operations.

Risk: Lifecycle actions such as start, stop, or reboot could disrupt workloads when run with over-privileged credentials or without operator confirmation.

Mitigation: Use least-privilege cloud credentials, require explicit confirmation for lifecycle actions, and record pre- and post-action status.

## Reference(s):

- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with operational summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes scoped, auditable ECS operations with pre- and post-action status summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
