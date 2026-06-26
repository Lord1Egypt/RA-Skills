## Description: <br>
Helps agents operate Tencent Cloud TKE clusters, Kubernetes resources, Pod troubleshooting workflows, Helm deployments, and TCR container registry resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect and administer Tencent Cloud TKE clusters, manage Kubernetes workloads, troubleshoot Pods, run Helm operations, manage RBAC tenants, and operate TCR registries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Tencent Cloud TKE, Kubernetes, Helm, RBAC, and TCR resources with broad infrastructure authority. <br>
Mitigation: Use least-privilege cloud and kubeconfig credentials, pass an explicit kubeconfig and namespace, and avoid production or administrator contexts by default. <br>
Risk: Delete, endpoint, Helm, RBAC, kubeconfig-add, token, and billing-related commands can change live infrastructure or cost-bearing resources. <br>
Mitigation: Require manual approval before executing these commands and prefer dry-run previews where supported. <br>
Risk: Generated tokens and kubeconfigs can expose live cluster access. <br>
Mitigation: Treat generated tokens and kubeconfigs as secrets and do not paste them into chats, logs, repositories, or shared tickets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencentcloud-tke-skill) <br>
- [Kubernetes tools installation guide](https://kubernetes.io/docs/tasks/tools/) <br>
- [Helm installation guide](https://helm.sh/docs/intro/install/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, YAML snippets, and structured status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run infrastructure administration commands that require explicit credentials and operator approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
