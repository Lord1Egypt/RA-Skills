## Description:

腾讯云跨账号资源迁移工具。将源账号（账号A）的 VPC、CLB、NAT、CVM、安全组等资源迁移到目标账号（账号B），通过 CCN 云联网实现跨账号网络互通。支持自动扫描、配置生成、Terraform 部署。

This skill is ready for commercial/non-commercial use.

## Publisher:

[awaili](https://clawhub.ai/user/awaili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to prepare and run Tencent Cloud cross-account resource migrations, including scanning source account resources, generating migration configuration, producing Terraform variables, and invoking Terraform workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes Tencent Cloud credentials in local YAML and Terraform variable/state files.

Mitigation: Use least-privilege, short-lived credentials in a controlled workspace; avoid previewing real secrets; restrict file permissions; and keep account.yaml, tc-migrate.yaml, terraform.tfvars, tfplan, and Terraform state files out of source control.

Risk: Terraform apply, run, destroy, and -y options can create, modify, or delete cloud resources.

Mitigation: Review generated configuration and Terraform plans before execution, avoid auto-approve until audited, and run only with an explicitly supplied and reviewed Terraform project.

Risk: The packaged artifact does not include the Terraform configuration directory expected by the docs and CLI.

Mitigation: Provide and audit the missing Terraform configuration before running init, plan, apply, run, destroy, or related commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awaili/skills/tc-migrate)
- [README](README.md)
- [Workflow guide](docs/workflow-guide.md)
- [Installation guide](reference/installation.md)
- [Command reference](reference/commands.md)
- [File structure reference](reference/file-structure.md)
- [CCN security reference](reference/ccn-security.md)
- [Troubleshooting guide](reference/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CLI instructions and local configuration/Terraform variable files when executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and src/pyproject.toml; package __version__ is 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
