## Description: <br>
Deploy a local project directory or Git repository to Volcengine as a running, reachable cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy local project directories or Git repositories to Volcengine ECS, VKE, or veFaaS after selecting a hosting mode and resource management path. It helps plan, provision, package, verify, and summarize cloud deployments with explicit approval and cleanup records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provision billable Volcengine cloud resources and expose services publicly. <br>
Mitigation: Review the generated .volcengine/deployment-plan.md and require explicit approval evidence before provisioning resources. <br>
Risk: Cloud credentials, connection strings, tokens, and generated service secrets could be exposed during deployment. <br>
Mitigation: Keep secrets out of logs and summaries, write generated local secret files with restrictive permissions, and keep local smoke-test credentials local-only. <br>
Risk: Failed or partial deployments can leave cloud resources running. <br>
Mitigation: Record CLI-created resources in .volcengine/created-resources.json and review reverse-order cleanup commands before deleting resources. <br>


## Reference(s): <br>
- [Volcengine Deploy on ClawHub](https://clawhub.ai/volc-sdk-team/skills/volcengine-deploy) <br>
- [Deployment Plan Template](artifact/references/deployment-plan-template.md) <br>
- [ECS Deployment Details](artifact/references/ecs-deploy-steps.md) <br>
- [VKE Deployment Details](artifact/references/vke-deploy-steps.md) <br>
- [veFaaS Skill Execution](artifact/references/faas-deploy-steps.md) <br>
- [Kubernetes manifest templates](artifact/references/k8s-manifests.md) <br>
- [Dockerfile templates](artifact/references/dockerfile-templates.md) <br>
- [Supported runtime dependencies](artifact/references/supported-dependencies.md) <br>
- [Deployment Service-Linked Roles](artifact/references/service-linked-roles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, Docker Compose, systemd, Dockerfile, and Kubernetes manifest snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local deployment state under .volcengine/ and emit cloud deployment summaries, health checks, logs, resource records, cleanup commands, and warnings.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
