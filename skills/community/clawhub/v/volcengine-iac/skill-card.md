## Description:

Use Terraform/IaC for Volcengine resources when the user explicitly chooses Terraform/IaC, already has a Terraform workflow or state, or needs plan, diff, drift, or destroy safety for managed infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to generate, validate, plan, apply, inspect, and destroy Terraform-managed Volcengine infrastructure when IaC is the chosen workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate Terraform against a Volcengine account and may create, change, replace, or destroy cloud resources.

Mitigation: Review every Terraform plan before apply or destroy, require explicit user confirmation, and avoid auto-approve workflows in real environments.

Risk: Terraform state, kubeconfig, credentials, and .volcengine/iac-outputs.json can contain sensitive infrastructure data.

Mitigation: Keep state and output files out of version control, restrict file permissions, and prefer encrypted remote state with strict access controls for shared or production use.

Risk: Volcengine TOS used through Terraform's S3 backend does not provide state locking.

Mitigation: Coordinate applies manually, use a single CI runner, or use a backend with locking for team-managed and production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volc-sdk-team/skills/volcengine-iac)
- [TOS S3-Compatible Backend](references/backend-tos.md)
- [Module Reference](references/modules.md)
- [Provider Versions](references/provider-versions.md)
- [VolcengineCC Blocked Resources](references/volcenginecc-blocked.md)
- [VKE Private CR Nginx Run](references/volcengine-vke-cr-nginx.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Terraform, shell, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Terraform working files, tfvars, backend configuration, plan summaries, drift reports, and infrastructure output files when the user chooses IaC.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
