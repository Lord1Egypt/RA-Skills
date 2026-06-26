## Description: <br>
Use Terraform/IaC for Volcengine resources only when the user explicitly chooses Terraform/IaC, already has a Terraform workflow/state, or confirms they need plan/diff/drift/destroy safety for VKE, managed databases/cache/storage, load balancers, domains/certificates, logging/monitoring, or team-managed infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to generate, review, apply, export, destroy, and drift-check Terraform-based Volcengine infrastructure when IaC is the chosen workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent make real Volcengine infrastructure changes through Terraform. <br>
Mitigation: Use least-privilege or temporary credentials, review every Terraform plan, and require explicit approval before apply or destroy. <br>
Risk: Terraform state, kubeconfig, cloud outputs, and generated files may contain sensitive infrastructure data or credentials. <br>
Mitigation: Keep Terraform state and .volcengine/iac-outputs.json out of git, logs, shared workspaces, and backups; use restrictive file permissions for sensitive outputs. <br>
Risk: Destructive Terraform operations can delete stateful resources such as databases, caches, or object storage. <br>
Mitigation: Reject auto-approve for apply and destroy, inspect plan summaries for deletes or replacements, and use an extra confirmation for production destroys. <br>


## Reference(s): <br>
- [TOS S3-Compatible Backend](references/backend-tos.md) <br>
- [Reusable Module Reference](references/modules.md) <br>
- [Provider Versions](references/provider-versions.md) <br>
- [Blocked Volcengine Cloud Control Resources](references/volcenginecc-blocked.md) <br>
- [Volcengine Cloud Control Network](references/volcenginecc-network.md) <br>
- [Volcengine Cloud Control ECS](references/volcenginecc-ecs.md) <br>
- [Volcengine Cloud Control VKE](references/volcenginecc-vke.md) <br>
- [Volcengine Cloud Control RDS MySQL](references/volcenginecc-rdsmysql.md) <br>
- [Volcengine Cloud Control Redis](references/volcenginecc-redis.md) <br>
- [Volcengine Cloud Control TOS](references/volcenginecc-tos.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Terraform configuration guidance, generated tfvars files, and JSON summaries from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Terraform working files under .volcengine/terraform/ and downstream output JSON at .volcengine/iac-outputs.json when used by an agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
