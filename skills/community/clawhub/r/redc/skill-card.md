## Description: <br>
RedC is a red-team infrastructure automation skill for deploying, managing, and monitoring cloud instances across Alibaba Cloud, AWS, Tencent Cloud, Volcengine, Huawei Cloud, Azure, and related providers through RedC, Terraform, and MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[No-Github](https://clawhub.ai/user/No-Github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, red-team operators, and cloud infrastructure engineers use this skill to plan, deploy, manage, monitor, and tear down red-team cloud infrastructure across multiple cloud providers through RedC and Terraform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud deployment and destroy actions can create cost, availability, or data exposure impact if run against production accounts or broad permissions. <br>
Mitigation: Use isolated lab accounts, scoped temporary credentials, and explicit approval for deploy, destroy, schedule, and billing-related actions. <br>
Risk: Templates and Terraform provisioners may execute scripts, open network access, or run local commands. <br>
Mitigation: Inspect template files, compare registry templates with their source, and run plan_case before start_case. <br>
Risk: The MCP server can expose powerful infrastructure operations if bound to an untrusted network. <br>
Mitigation: Keep MCP on local stdio or bind SSE only to 127.0.0.1. <br>
Risk: Outputs may include credentials, SSH details, billing information, or infrastructure identifiers. <br>
Mitigation: Review outputs before sharing and avoid pasting long-lived root or owner keys into chat. <br>


## Reference(s): <br>
- [RedC project homepage](https://github.com/wgpsec/redc) <br>
- [RedC template registry](https://redc.wgpsec.org) <br>
- [Terraform downloads](https://developer.hashicorp.com/terraform/downloads) <br>
- [ClawHub skill page](https://clawhub.ai/No-Github/redc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples, tool arguments, Terraform plan guidance, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference cloud credentials, billing data, SSH connection details, Terraform outputs, and deployment state; review sensitive outputs before sharing.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
