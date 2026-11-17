## Description:

RedC helps agents deploy, manage, and monitor red-team cloud infrastructure across Alibaba Cloud, AWS, Tencent Cloud, Volcengine, Huawei Cloud, Azure, and related providers through RedC and Terraform workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no-github](https://clawhub.ai/user/no-github)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and red teams use this skill to plan, deploy, operate, and tear down multi-cloud red-team infrastructure. It is suited for workflows that require template inspection, Terraform planning, remote access details, cost checks, and lifecycle management for cloud instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, modify, or destroy real cloud infrastructure and may incur cost or affect live accounts.

Mitigation: Use a throwaway or tightly scoped cloud account, temporary credentials, and review the Terraform plan before any start_case or compose_up action.

Risk: Cloud provider credentials are required for the selected provider and could expose sensitive account access if mishandled.

Mitigation: Configure only the provider credentials needed for the current deployment, prefer short-lived scoped credentials, and do not paste long-lived root or owner keys into chat.

Risk: Terraform templates can contain remote-exec, local-exec, cloud-init, user_data, and open security group rules.

Mitigation: Inspect template files with get_template_info, use plan_case before deployment, and pin templates to trusted sources.

Risk: The MCP server can expose infrastructure-management tools if bound to an untrusted network.

Mitigation: Use stdio transport when possible; if SSE mode is required, bind only to 127.0.0.1.

Risk: Unverified redc or Terraform binaries can introduce supply-chain risk.

Mitigation: Download redc from official GitHub releases and Terraform from HashiCorp, then verify the published checksums or signatures.

## Reference(s):

- [ClawHub redc skill page](https://clawhub.ai/no-github/skills/redc)
- [Publisher profile](https://clawhub.ai/user/no-github)
- [RedC GitHub project](https://github.com/wgpsec/redc)
- [RedC template registry](https://redc.wgpsec.org)
- [RedC template source](https://github.com/wgpsec/redc-template)
- [RedC releases](https://github.com/wgpsec/redc/releases)
- [Terraform downloads](https://developer.hashicorp.com/terraform/downloads)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands, configuration values, and MCP tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud resource plans, status summaries, credentials handling guidance, SSH connection details, cost estimates, and deployment lifecycle instructions.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
