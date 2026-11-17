## Description:

Tencent Cloud TKE container-service operations skill for cluster management, Kubernetes resource operations, Pod troubleshooting, Helm deployments, and TCR registry management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect and administer Tencent Cloud TKE clusters, Kubernetes workloads, Helm releases, tenant RBAC, kubeconfig access, and TCR registry resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or persist powerful Tencent Cloud and Kubernetes credentials, including kubeconfigs and tenant tokens.

Mitigation: Install only in a trusted operator environment, avoid passing secrets on the command line, review resolved kubeconfig and target cluster before use, and shorten tenant token lifetimes.

Risk: The skill can perform write operations such as endpoint changes, Kubernetes apply/delete/create, Helm install/upgrade/uninstall, RBAC tenant changes, and TCR create/delete actions.

Mitigation: Prefer dry-run previews where available and confirm the target region, namespace, cluster, registry, and resource identifiers before executing write or delete commands.

Risk: Default tenant RBAC templates include access to Kubernetes Secrets and can grant broad namespace control.

Mitigation: Remove Secret access from default tenant roles unless explicitly needed, review custom RBAC rules before use, and apply least-privilege role bindings.

## Reference(s):

- [Kubernetes kubectl installation documentation](https://kubernetes.io/docs/tasks/tools/)
- [Helm installation documentation](https://helm.sh/docs/intro/install/)
- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencentcloud-tke-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include kubectl, helm, Tencent Cloud API command guidance, generated kubeconfig snippets, RBAC manifests, and operational summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
