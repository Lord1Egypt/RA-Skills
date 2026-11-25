## Description:

Use when the user asks to analyze, consult, setup, manage, configure, or design a Volcengine Landing Zone, including organization, accounts, finance, identity, cloudtrail, or network infrastructure, or to deploy a solution/blueprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud platform developers and engineers use this skill to design and manage Volcengine landing zones, create accounts and baselines, and deploy solution blueprints. It provides planning guidance and execution workflows for organization, finance, identity, audit, and network foundations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags concerns about targeting the intended cloud account and persistent privileges, and scanner coverage is incomplete.

Mitigation: Review account targets and privilege scope in the proposed configuration and plan, resolve the flagged undeclared capabilities and unresolved paths, and defer installation until these concerns have been reviewed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/volc-sdk-team/skills/volcengine-landing-zone)
- [Publisher profile](https://clawhub.ai/user/volc-sdk-team)
- [Landing Zone setup guidebook](references/landing-zone-setup/guidebook.md)
- [Account Factory guidebook](references/account-factory/guidebook.md)
- [Solution Deployment guidebook](references/solution-deployment/guidebook.md)
- [Preflight checks](references/preflight-checks.md)
- [Failure recovery guide](references/failure-recovery.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, JSON architecture and hand-off files, Terraform HCL, shell commands, and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployable infrastructure configuration and execution plans.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
