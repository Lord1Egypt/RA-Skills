## Description: <br>
Use for SySelf Autopilot on Hetzner: management kubeconfig setup, organization namespace, Hetzner account preparation, ClusterStack and Cluster manifests, bare metal worker onboarding with HetznerBareMetalHost, day-2 cluster operations, and support-boundary-aware troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SergeyKDEV](https://clawhub.ai/user/SergeyKDEV) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to prepare and operate managed SySelf Autopilot clusters on Hetzner, including management-cluster access, Hetzner credentials, bare metal host onboarding, ClusterStack releases, workload cluster creation, and day-2 operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that use powerful Hetzner cloud and Kubernetes credentials. <br>
Mitigation: Use least-privilege Hetzner credentials, keep tokens and kubeconfigs private, and confirm the current kubectl context and namespace before running commands. <br>
Risk: Bundled scripts and templates can create persistent Kubernetes secrets and cluster resources. <br>
Mitigation: Inspect the shell scripts and YAML templates before execution and apply them only to the intended SySelf Autopilot management cluster. <br>
Risk: Unsupported infrastructure assumptions can lead to failed SySelf Autopilot cluster operations. <br>
Mitigation: Stay within official SySelf Autopilot documentation and stop rather than improvising when a requested step is not documented or supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SergeyKDEV/syself-autopilot-hetzner) <br>
- [SySelf Autopilot introduction](https://syself.com/docs/hetzner/apalla/getting-started/introduction-to-syself-autopilot) <br>
- [Accessing the management cluster](https://syself.com/docs/hetzner/apalla/getting-started/accessing-the-management-cluster) <br>
- [Hetzner account preparation](https://syself.com/docs/hetzner/apalla/getting-started/hetzner-account-preparation) <br>
- [Creating clusters](https://syself.com/docs/hetzner/apalla/getting-started/creating-clusters) <br>
- [Cluster stacks](https://syself.com/docs/hetzner/apalla/concepts/cluster-stacks) <br>
- [Bare metal concepts](https://syself.com/docs/hetzner/apalla/concepts/baremetal) <br>
- [Adding bare metal servers](https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/adding-baremetal-servers-to-your-cluster) <br>
- [Bare metal troubleshooting](https://syself.com/docs/hetzner/apalla/troubleshooting/baremetal-servers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and Kubernetes YAML guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference bundled shell scripts and YAML templates for SySelf Autopilot and Hetzner workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
