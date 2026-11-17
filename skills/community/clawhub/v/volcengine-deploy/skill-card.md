## Description:

Deploy a local project directory or Git repository to Volcengine as a running, reachable cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, provision, deploy, and verify applications on Volcengine ECS, VKE, or veFaaS. It is intended for deployments that need resource planning, approval gates, runtime configuration, cloud-resource tracking, and post-deploy health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify real Volcengine resources and may incur cost or expose services.

Mitigation: Review the deployment plan before provisioning, require explicit approval for resource creation, and use project-scoped, short-lived Volcengine credentials.

Risk: Deployment of untrusted repositories can execute builds, shell commands, and remote commands.

Mitigation: Run untrusted builds in an isolated environment and validate repository, service, and resource names before using them in remote commands.

Risk: Runtime configuration may include kubeconfig files, connection strings, access keys, or plaintext Kubernetes Secret manifests.

Mitigation: Avoid committing kubeconfig or plaintext Secret manifests, do not print secrets in logs, and store generated local files with restricted permissions.

Risk: The generated smoke-test compose stack may expose dependency ports and default test credentials.

Mitigation: Run smoke tests only on isolated hosts or tighten ports and credentials before using the compose stack on a reachable machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-deploy)
- [Deployment Plan Template](references/deployment-plan-template.md)
- [Dockerfile Templates](references/dockerfile-templates.md)
- [ECS Deployment Details](references/ecs-deploy-steps.md)
- [veFaaS Skill Execution](references/faas-deploy-steps.md)
- [Kubernetes Manifest Templates](references/k8s-manifests.md)
- [Deployment Service-Linked Roles](references/service-linked-roles.md)
- [Supported Runtime Dependencies](references/supported-dependencies.md)
- [VKE Deployment Details](references/vke-deploy-steps.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON resource ledgers, generated configuration files, and deployment manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .volcengine state, deployment plans, Docker/Kubernetes/systemd files, and cloud resources after user approval.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
