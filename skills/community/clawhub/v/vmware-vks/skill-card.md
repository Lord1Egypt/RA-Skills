## Description: <br>
Use this skill to manage vSphere Kubernetes Service (VKS), including Supervisor clusters, vSphere Namespaces, TKC cluster lifecycle, kubeconfig retrieval, and Harbor registry checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect VKS readiness, manage vSphere Namespaces, and create, scale, upgrade, or delete TKC clusters in vSphere environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent sensitive cluster credentials and production-changing VKS/TKC powers. <br>
Mitigation: Install only for intended VMware administration use, use least-privilege vCenter accounts, and require human approval before production scale, upgrade, delete, or credential-retrieval actions. <br>
Risk: Kubeconfig output can expose short-lived vCenter session tokens if pasted into chat or stored carelessly. <br>
Mitigation: Write kubeconfig output to local files with restrictive permissions and avoid displaying token contents in conversation context. <br>
Risk: TLS verification can be disabled for self-signed vCenter certificates. <br>
Mitigation: Keep TLS verification enabled where possible and limit disabled verification to controlled environments with known certificate posture. <br>
Risk: Destructive namespace or TKC operations can disrupt workloads. <br>
Mitigation: Use dry-run plans, explicit confirmations, workload checks, audit logs, and policy rules before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-vks) <br>
- [VMware VKS Source](https://github.com/zw008/VMware-VKS) <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with CLI commands, configuration snippets, and structured tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce YAML plans, kubeconfig file paths, or MCP-style structured results depending on the workflow.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
