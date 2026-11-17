## Description:

Software deployment workflow for systems with separate UAT and PROD environments, covering bug fix planning, deploy flow selection, emergency hotfixes, rollbacks, nightly pipelines, approval gates, human checkpoints, notifications, and rollback procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonylnng](https://clawhub.ai/user/tonylnng)

### License/Terms of Use:


## Use Case:

Developers, release managers, and operations teams use this skill to choose and execute safe deployment paths across separate UAT and PROD environments. It supports routine bug-fix deployments, version-mismatch decisions, emergency hotfix handling, rollback planning, and post-deploy monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled automation could deploy or roll back production changes based on status transitions without a fresh approval gate for each live action.

Mitigation: Require explicit authorized approval immediately before every PROD deploy or rollback, and separate status tracking from deploy authority.

Risk: Production deployment guidance can be unsafe if release artifacts, freeze windows, or rollback readiness are not checked before execution.

Mitigation: Enforce freeze checks, validate release artifacts, maintain audit logs, and confirm rollback paths before any production action.

Risk: Operator notifications may be missed or misunderstood during high-impact deploys or rollbacks.

Mitigation: Localize notification templates for receiving operators and verify that the right channels and on-call responders are configured.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with workflow diagrams, checklists, tables, notification templates, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment process guidance rather than executable automation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
