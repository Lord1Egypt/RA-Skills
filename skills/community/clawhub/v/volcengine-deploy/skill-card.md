## Description:

Deploy a local project directory or Git repository to Volcengine as a running, reachable cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy a local project or Git repository to Volcengine through ECS, VKE, or veFaaS, with deployment choices and resources recorded for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial: 9 of 12 components were fully inspected, and ClawScan reports deployment risks.

Mitigation: Review generated scripts, plans, and deployment configuration before executing them; the available scan does not cover every component.

Risk: Generated smoke-test Compose files publish application and dependency ports on host interfaces, which can expose test services and credentials.

Mitigation: Run the test stack only in a trusted local environment; bind or restrict published ports and avoid exposing test services publicly.

Risk: Deployment packaging can include project files that were not intended for release.

Mitigation: Review the build or archive context and exclude credentials, local environment files, and unrelated files before packaging.

Risk: Deployment configuration handles credentials and changes network access, permissions, and database state.

Mitigation: Keep secrets out of plans and logs, use the designated environment or Secret path with restrictive file permissions, prefer private endpoints and narrow allowlists, and review migration and permission changes.

Risk: Provisioning creates billable resources and may open services to public traffic.

Mitigation: Complete the validated deployment plan and obtain explicit resource-creation approval; limit ingress to required ports and trusted source ranges.

## Reference(s):

- [Deployment plan template](artifact/references/deployment-plan-template.md)
- [ECS deployment steps](artifact/references/ecs-deploy-steps.md)
- [VKE deployment steps](artifact/references/vke-deploy-steps.md)
- [veFaaS deployment steps](artifact/references/faas-deploy-steps.md)
- [Kubernetes manifests](artifact/references/k8s-manifests.md)
- [Supported dependencies](artifact/references/supported-dependencies.md)
- [Dockerfile templates](artifact/references/dockerfile-templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Deployment guidance]

**Output Format:** [Markdown plans and reports, shell commands, and generated JSON or deployment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable commands and resource, container, or Kubernetes configuration.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
