## Description: <br>
腾讯云跨账号资源迁移工具。将源账号（账号A）的 VPC、CLB、NAT、CVM、安全组等资源迁移到目标账号（账号B），通过 CCN 云联网实现跨账号网络互通。支持自动扫描、配置生成、Terraform 部署。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awaili](https://clawhub.ai/user/awaili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud infrastructure engineers use this skill to scan Tencent Cloud resources in a source account, generate migration configuration, and apply Terraform to recreate selected VPC, subnet, security group, CLB, NAT, CVM, and CCN resources in a target account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool uses source and destination Tencent Cloud credentials and writes sensitive configuration and Terraform state files. <br>
Mitigation: Use temporary least-privilege credentials, keep account.yaml, tc-migrate.yaml, terraform.tfvars, tfplan, and terraform.tfstate out of version control, and restrict local file permissions. <br>
Risk: Terraform actions can create, modify, or destroy cloud infrastructure. <br>
Mitigation: Review Terraform plan output before apply or destroy, and avoid --yes in production workflows. <br>
Risk: Migrated security-group behavior may need manual review, especially IPv6 rules. <br>
Mitigation: Verify security-group rules manually after migration before relying on the migrated network posture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awaili/tc-migrate) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Workflow guide](artifact/docs/workflow-guide.md) <br>
- [Command reference](artifact/reference/commands.md) <br>
- [CCN security configuration](artifact/reference/ccn-security.md) <br>
- [Installation guide](artifact/reference/installation.md) <br>
- [Troubleshooting guide](artifact/reference/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML examples, and Terraform configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux, Python 3, Terraform, and Tencent Cloud credentials for both source and target accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
