## Description:

Use when the user asks to analyze, consult, setup, manage, configure, or design a Volcengine Landing Zone, including organization, accounts, finance, identity, cloudtrail, or network infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud platform engineers, and consultants use this skill to design and operate Volcengine landing zones, including organization setup, account factory workflows, baseline application, and failure recovery. It supports read-only consulting as well as gated infrastructure execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run privileged Volcengine infrastructure changes.

Mitigation: Use short-lived least-privilege credentials and review Terraform plans before applying changes.

Risk: Workspace baseline packages can override built-in baseline packages when names collide.

Mitigation: Verify the resolved package source and review package contents before baseline apply.

Risk: Credential material or generated administrator password files may be exposed if handled carelessly.

Mitigation: Keep credentials outside chat and repositories, and protect or delete generated password files after first use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/volc-sdk-team/skills/volcengine-landing-zone)
- [Preflight Checks](references/preflight-checks.md)
- [Volcengine Landing Zone Setup Guide](references/landing-zone-setup/guidebook.md)
- [Account Factory Workflow](references/account-factory/guidebook.md)
- [Failure Recovery](references/failure-recovery.md)
- [Account Factory Baseline Schema](references/account-factory/baseline.schema.json)
- [Volcengine CLI README](https://github.com/volcengine/volcengine-cli/blob/master/README.MD)
- [Volcengine Terraform Provider README](https://github.com/volcengine/terraform-provider-volcenginecc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, Terraform configuration guidance, JSON runtime files, and generated HTML review files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace-scoped execution files, Terraform variable files, status JSON, login information, baseline plans, and setup reports during authorized runs]

## Skill Version(s):

1.0.3 (source: release evidence changelog and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
