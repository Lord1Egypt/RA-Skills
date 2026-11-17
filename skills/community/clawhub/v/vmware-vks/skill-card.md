## Description:

Use this skill to manage vSphere Kubernetes Service (VKS) Supervisor clusters, vSphere Namespaces, and Tanzu Kubernetes Cluster (TKC) lifecycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use the skill to inspect VKS environments and manage Supervisor namespaces and TKC clusters through the VMware VKS CLI or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because it handles powerful credentials and review of a referenced file was incomplete; the scan does not establish whether the skill is malicious or safe.

Mitigation: Review the skill and referenced content before installation, and treat the scanner result as an unresolved signal.

Risk: An unpinned installation command can install a different package release, and exported kubeconfigs contain sensitive access material.

Mitigation: Review and pin the package version before installing. Retrieve a kubeconfig only on explicit request and save it to an owner-only file rather than printing it.

## Reference(s):

- [VMware VKS project homepage (metadata)](https://github.com/vmware-skills/VMware-VKS)
- [Capabilities](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown summaries and structured tool results; optional kubeconfig file when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A kubeconfig contains sensitive access credentials and should be saved to an owner-only file.]

## Skill Version(s):

3.7.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
