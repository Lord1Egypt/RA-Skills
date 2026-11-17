## Description:

Guides agents through SySelf Autopilot operations on Hetzner, including management kubeconfig setup, credential preparation, ClusterStack and Cluster manifests, bare metal worker onboarding, day-2 operations, and support-boundary-aware troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeykdev](https://clawhub.ai/user/sergeykdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to create, operate, and troubleshoot managed SySelf Autopilot clusters on Hetzner. It is focused on management-cluster access, Hetzner credential setup, Kubernetes manifests, bare metal worker onboarding, and supported day-2 operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can create Kubernetes secrets or apply infrastructure manifests against whichever Kubernetes context is active.

Mitigation: Before running scripts, set an explicit kubeconfig, context, and namespace; verify the API server and organization namespace before applying manifests or creating secrets.

Risk: Hetzner cloud, Robot, and SSH credentials may be uploaded to the wrong cluster or exposed through less controlled secret creation flows.

Mitigation: Use a controlled credential handling process where possible, avoid unintended namespaces, and rotate Hetzner or SSH credentials if they may have been submitted to the wrong cluster.

Risk: Unsupported SySelf or Hetzner infrastructure assumptions can lead to failed provisioning or misleading remediation steps.

Mitigation: Keep troubleshooting inside the official SySelf Autopilot documentation and stop when a requested step is unsupported or undocumented.

## Reference(s):

- [SySelf Autopilot introduction](https://syself.com/docs/hetzner/apalla/getting-started/introduction-to-syself-autopilot)
- [Accessing the management cluster](https://syself.com/docs/hetzner/apalla/getting-started/accessing-the-management-cluster)
- [Hetzner account preparation](https://syself.com/docs/hetzner/apalla/getting-started/hetzner-account-preparation)
- [Creating clusters](https://syself.com/docs/hetzner/apalla/getting-started/creating-clusters)
- [ClusterStacks](https://syself.com/docs/hetzner/apalla/concepts/cluster-stacks)
- [Management and workload clusters](https://syself.com/docs/hetzner/apalla/concepts/mgt-and-wl-clusters)
- [Bare metal concept](https://syself.com/docs/hetzner/apalla/concepts/baremetal)
- [Adding bare metal servers](https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/adding-baremetal-servers-to-your-cluster)
- [HCloud server management](https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/hcloud-server-management)
- [Removing specific nodes](https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/remove-specific-nodes)
- [Rebooting bare metal servers](https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/rebooting-baremetal-servers)
- [High availability Kubernetes control plane](https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-configuration/ha-kubernetes-controlplane)
- [Cluster Autoscaler](https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-autoscaler)
- [Bare metal troubleshooting](https://syself.com/docs/hetzner/apalla/troubleshooting/baremetal-servers)
- [Wiping bare metal server disks](https://syself.com/docs/hetzner/apalla/troubleshooting/wiping-baremetal-server-disks)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and Kubernetes YAML templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes support-boundary checks, required input validation, and context-specific operational next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
