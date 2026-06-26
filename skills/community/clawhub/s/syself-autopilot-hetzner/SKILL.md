---
name: syself-autopilot-hetzner
description: "Use for SySelf Autopilot on Hetzner: management kubeconfig setup, organization namespace, Hetzner account preparation, ClusterStack and Cluster manifests, bare metal worker onboarding with HetznerBareMetalHost, day-2 cluster operations, and support-boundary-aware troubleshooting. Invoke for SySelf Autopilot, Hetzner, bare metal workers, HetznerBareMetalHost, ClusterStack, management cluster, workload cluster, Robot, and HCloud-backed cluster tasks."
argument-hint: "[access|prepare-hetzner|register-baremetal|create-cluster|operate|troubleshoot]"
---

# SySelf Autopilot on Hetzner

## When to Use
- Creating or operating a managed SySelf Autopilot cluster on Hetzner.
- Preparing management-cluster access and setting the organization namespace in kubeconfig.
- Preparing Hetzner HCloud and Robot credentials for SySelf Autopilot.
- Registering and selecting bare metal worker nodes through `HetznerBareMetalHost`.
- Applying `ClusterStack`, `HetznerClusterStackReleaseTemplate`, and `Cluster` manifests.
- Running day-2 operations such as scaling, HA changes, targeted node removal, bare metal maintenance, and supported troubleshooting.

## Do Not Use For
- Self-managed CAPH bootstrap flows using `kind`, `clusterctl init`, or `clusterctl move`.
- Generic Hetzner CLI work without SySelf context.
- Unsupported infrastructure designs that SySelf support has already rejected.
- Inventing undocumented SySelf behavior, upgrade steps, or bootstrap fixes.

## Companion Skill
Load `hetzner-cloud` whenever the task involves HCloud CLI work.

Use `hetzner-cloud` for:
- validating HCloud access, context, regions, server types, SSH keys, snapshots, and servers
- recommending or executing `hcloud` commands
- HCloud-side safety rules and confirmation flow

Inherit these rules from `hetzner-cloud`:
- never expose tokens or credentials
- ask for confirmation before create or modify actions
- show the exact `hcloud` command before execution
- suggest snapshots before risky HCloud-side changes

`syself-autopilot-hetzner` is the source of truth for the SySelf workflow and support boundaries.
`hetzner-cloud` is the source of truth for safe HCloud CLI usage inside that workflow.

## Source of Truth
Use only official SySelf Autopilot docs as authoritative guidance.

Core starting points:
- https://syself.com/docs/hetzner/apalla/getting-started/introduction-to-syself-autopilot
- https://syself.com/docs/hetzner/apalla/getting-started/accessing-the-management-cluster
- https://syself.com/docs/hetzner/apalla/getting-started/hetzner-account-preparation
- https://syself.com/docs/hetzner/apalla/getting-started/creating-clusters

Core concepts:
- https://syself.com/docs/hetzner/apalla/concepts/cluster-stacks
- https://syself.com/docs/hetzner/apalla/concepts/mgt-and-wl-clusters
- https://syself.com/docs/hetzner/apalla/concepts/baremetal
- https://syself.com/docs/hetzner/apalla/concepts/self-healing

Core bare metal and operations guides:
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/adding-baremetal-servers-to-your-cluster
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/hcloud-server-management
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/remove-specific-nodes
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/rebooting-baremetal-servers
- https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-configuration/baremetal-control-planes
- https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-configuration/ha-kubernetes-controlplane
- https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-autoscaler

Core troubleshooting:
- https://syself.com/docs/hetzner/apalla/troubleshooting/baremetal-servers
- https://syself.com/docs/hetzner/apalla/troubleshooting/wiping-baremetal-server-disks

If the docs do not cover a step, say so explicitly and stop short of improvising.

## Operating Model
Assume the managed SySelf Autopilot model unless the user explicitly says otherwise.

Managed by SySelf:
- hosted management cluster
- tested ClusterStack-based release flow
- lifecycle reconciliation for workload clusters
- software installation on bare metal nodes
- supported self-healing and supported update paths

Owned by the user or operator:
- obtaining access to SySelf Autopilot
- obtaining the management kubeconfig
- setting the organization namespace in kubeconfig
- Hetzner project, tokens, Robot credentials, and SSH keys
- buying, exchanging, and validating hardware
- decisions around unsupported infrastructure patterns

## Workflow

### 1. Identify the mode
- Confirm the user is using SySelf Autopilot.
- If they ask for `kind`, `clusterctl init`, bootstrap clusters, or pivoting, explain that those are self-managed CAPH patterns and not the default path for this skill.

### 2. Prepare management-cluster access
- Obtain the management kubeconfig from SySelf admins, or from the gated `kubeconfig.yaml` resource on the official access page if the user is authenticated there.
- Save it locally.
- Replace the namespace with the SySelf organization namespace.
- Set file permissions with `chmod 600`.
- Export `KUBECONFIG`.
- Validate login with `kubectl get clusters`.

Important:
- The official access page clearly shows a gated `kubeconfig.yaml` resource.
- Outside an authenticated docs session, do not assume a public direct download URL exists.
- Safe fallback: ask SySelf admins for the kubeconfig.

### 3. Prepare local tooling
Expected tools:
- `kubectl`
- `kubelogin`
- `helm`
- `hcloud` when automating Hetzner steps

Recommended checks:
```bash
kubectl version --client
kubectl oidc-login --help >/dev/null
helm version
hcloud version
```

### 4. Prepare Hetzner account and credentials
- Load `hetzner-cloud` before recommending or executing `hcloud` commands.
- Create or select the HCloud project.
- Create a read-write HCloud token.
- Upload the SSH key to HCloud.
- Create the Hetzner Robot webservice user.
- Export the required environment variables.

Expected variables:
- `HCLOUD_TOKEN`
- `HETZNER_ROBOT_USER`
- `HETZNER_ROBOT_PASSWORD`
- `SSH_KEY_NAME`
- `HETZNER_SSH_PUB_PATH`
- `HETZNER_SSH_PRIV_PATH`
- `CLUSTER_NAME`
- `HCLOUD_REGION`
- `CONTROL_PLANE_MACHINE_TYPE_HCLOUD`

### 5. Create SySelf management-cluster secrets
Create:
- `hetzner` secret for HCloud and Robot credentials
- `robot-ssh` secret for bare metal SSH provisioning

Preferred asset:
- `scripts/02-create-management-secrets.sh`

### 6. Run bare metal preflight
Before any bare metal onboarding, verify all of the following.

- The server is not blocked by the Legacy BIOS requirement.
- RAID state is compatible, or disks were wiped per the official guide.
- The SSH key name in Hetzner matches the one used in the secret.
- The user is not depending on unsupported firewall or vSwitch behavior for the failing bootstrap path.

Stop if:
- the server is EFI-only and cannot support the required boot mode
- the user expects unsupported Hetzner firewall or vSwitch behavior to be part of the supported baseline

### 7. Register bare metal hosts
- Create one `HetznerBareMetalHost` per server.
- Always prefer explicit labels for cluster scope and role.
- Add `rootDeviceHints.wwn` when known.
- If WWN is not known, apply without it first, inspect status, then update.

Preferred assets:
- `templates/hetznerbaremetalhost.yaml`
- `scripts/04-register-baremetal-hosts.sh`

Useful checks:
```bash
kubectl get hetznerbaremetalhost
kubectl describe hetznerbaremetalhost <name>
kubectl get hbmh <name> -o yaml | yq .status.hardwareDetails.storage
lsblk -o name,WWN
```

### 8. Create ClusterStack release objects
- Apply the `ClusterStack` and `HetznerClusterStackReleaseTemplate`.
- Wait for the `ClusterStackRelease` to become ready before creating the workload cluster.

Preferred asset:
- `templates/clusterstack.yaml`

Useful checks:
```bash
kubectl get clusterstack
kubectl get clusterstackreleases
kubectl get HetznerNodeImageReleases
```

### 9. Create the workload cluster
- Apply the cluster manifest in the management cluster.
- Default supported worker pattern in this skill: HCloud control planes plus `workeramd64baremetal` workers.
- Use `workerHostSelectorBareMetal` with `matchLabels`.

Preferred assets:
- `templates/cluster.yaml`
- `scripts/05-apply-cluster.sh`

Useful checks:
```bash
kubectl get cluster
kubectl get machines
kubectl get machines -w
```

### 10. Fetch workload kubeconfig and verify access
- Use the current official Autopilot docs version to obtain the documented workload-kubeconfig retrieval command.
- Do not invent a replacement command if the docs snippet is unavailable.
- After retrieving the kubeconfig, export it and verify access.

Preferred asset:
- `scripts/06-verify-workload-access.sh`

Useful checks:
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
```

### 11. Day-2 operations

Add bare metal workers:
- add more `HetznerBareMetalHost` resources
- add or scale `workeramd64baremetal` MachineDeployments
- prefer `workerHostSelectorBareMetal` with `matchLabels`

Scale HCloud workers:
- edit `spec.topology.workers.machineDeployments[].replicas`
- use separate MachineDeployments per machine type

Increase control plane HA:
- set `spec.topology.controlPlane.replicas` to an odd number
- prefer 3 or 5

Remove specific nodes:
- annotate the Cluster API `Machine` with `cluster.x-k8s.io/delete-machine=""`
- then reduce the corresponding replica count

Reboot bare metal nodes in-place:
- pause the `Machine` in the management cluster
- drain and later uncordon the node in the workload cluster
- remove the pause annotation after maintenance

Autoscaling:
- use Cluster Autoscaler in the workload cluster
- a strong pattern is bare metal base capacity plus HCloud burst capacity

Upgrades:
- always switch docs version to the cluster’s current version before following upgrade instructions
- do not invent upgrade steps not shown for that version

## Support-Verified Constraints
Treat these as hard rules unless official SySelf docs or SySelf support explicitly supersede them.

1. UEFI-only bare metal servers without the required boot-mode path are unsupported for this provisioning flow.
2. Hetzner firewall and vSwitch were identified by SySelf support as unsupported in the reported failing bootstrap scenario.
3. A cluster with cloud control planes and only bare metal workers can leave the hcloud CSI controller unschedulable.

Supported response for that CSI case:
- ignore hcloud CSI if it is not needed
- add at least one cloud worker node
- knowingly allow scheduling on the control plane if the user understands the tradeoff

Do not claim support for:
- undocumented OCI credential fixes
- undocumented MachineHealthCheck pause behavior
- undocumented bootstrap annotations or reconciliation overrides

## Troubleshooting Order

Bare metal registration or bootstrap failure:
1. boot-mode compatibility
2. RAID or stale disk state
3. SSH key mismatch
4. unsupported firewall or vSwitch assumptions
5. `HetznerBareMetalHost` status and hardware details

MachineHealthCheck loops:
1. verify supported baseline first
2. remove unsupported network assumptions
3. inspect runtime objects before proposing remediation

Stuck HCloud control plane provisioning:
1. consider regional HCloud capacity issues
2. do not switch control plane class casually, because that triggers rolling replacement

## Assets
- `templates/management-kubeconfig.yaml`
- `templates/clusterstack.yaml`
- `templates/cluster.yaml`
- `templates/hetznerbaremetalhost.yaml`
- `scripts/01-validate-access.sh`
- `scripts/02-create-management-secrets.sh`
- `scripts/03-prepare-management-kubeconfig.sh`
- `scripts/04-register-baremetal-hosts.sh`
- `scripts/05-apply-cluster.sh`
- `scripts/06-verify-workload-access.sh`

## Anti-Patterns
- Do not use `kind`, `clusterctl init`, or `clusterctl move` for the managed Autopilot path.
- Do not use unlabeled bare metal host selection for production.
- Do not present self-managed CAPH examples as the default SySelf Autopilot workflow.
- Do not present unsupported Hetzner firewall or vSwitch designs as supported SySelf baseline.
- Do not promise public direct kubeconfig download URLs unless they are visible and authenticated in the docs session.

## Output Format
When using this skill, respond in this order:
1. current mode and scope
2. missing inputs or blockers
3. next supported action
4. exact commands or assets to use
5. risks, boundaries, or support constraints

## Completion Criteria
Consider the main flow complete when all of the following are true:
- management kubeconfig is present and scoped to the organization namespace
- management-cluster access works
- Hetzner secrets exist in the management cluster
- `HetznerBareMetalHost` resources are applied and validated
- intended `ClusterStackRelease` is ready
- workload cluster manifest is applied
- workload cluster access works with kubeconfig
- further guidance remains inside supported SySelf boundaries
---
name: syself
description: Use when deploying, managing, troubleshooting, or evolving a managed SySelf Autopilot cluster on Hetzner, especially with bare metal worker nodes. Covers the full official Autopilot flow from management-cluster access and Hetzner preparation through ClusterStack, cluster manifests, bare metal host onboarding, day-2 operations, and support-boundary-aware troubleshooting.
license: MIT
metadata:
  author: ""
  version: "2.0.0"
  domain: platform-engineering
  triggers: SySelf, Autopilot, Hetzner, bare metal, HetznerBareMetalHost, ClusterStack, workload cluster, management cluster, Robot, HCloud, bare metal workers, cluster management
  role: engineer
  scope: implementation
  output-format: code
  related-skills: hetzner-cloud
---

# SKILL: SySelf Autopilot on Hetzner with Bare Metal Workers

## Purpose
This skill equips an agent to act as a reliable execution and guidance layer for
the official SySelf Autopilot workflow on Hetzner, with special attention to
bare metal worker nodes.

This skill is for the managed SySelf Autopilot model, not for self-managed CAPH
bootstrap clusters. Use it when the goal is to create or manage a workload
cluster through the SySelf-hosted management cluster.

## Source of Truth
Use only official SySelf Autopilot documentation as the primary source of truth:
- https://syself.com/docs/hetzner/apalla/getting-started/introduction-to-syself-autopilot
- https://syself.com/docs/hetzner/apalla/getting-started/prerequisites
- https://syself.com/docs/hetzner/apalla/getting-started/accessing-the-management-cluster
- https://syself.com/docs/hetzner/apalla/getting-started/hetzner-account-preparation
- https://syself.com/docs/hetzner/apalla/getting-started/creating-clusters
- https://syself.com/docs/hetzner/apalla/concepts/cluster-stacks
- https://syself.com/docs/hetzner/apalla/concepts/mgt-and-wl-clusters
- https://syself.com/docs/hetzner/apalla/concepts/baremetal
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/adding-baremetal-servers-to-your-cluster
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/hcloud-server-management
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/remove-specific-nodes
- https://syself.com/docs/hetzner/apalla/how-to-guides/server-management/rebooting-baremetal-servers
- https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-configuration/baremetal-control-planes
- https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-configuration/ha-kubernetes-controlplane
- https://syself.com/docs/hetzner/apalla/how-to-guides/cluster-autoscaler
- https://syself.com/docs/hetzner/apalla/concepts/self-healing
- https://syself.com/docs/hetzner/apalla/troubleshooting/baremetal-servers
- https://syself.com/docs/hetzner/apalla/troubleshooting/wiping-baremetal-server-disks

If a task would require assumptions not covered by the official docs, state that
explicitly and stop short of inventing behavior.

## Required Companion Skill
This skill must actively rely on the `hetzner-cloud` skill for all HCloud CLI
operations and HCloud safety practices.

Use `hetzner-cloud` whenever the task includes any of the following:
- validating HCloud access or context
- listing projects, regions, server types, SSH keys, snapshots, or servers
- creating or checking HCloud SSH keys
- inspecting HCloud capacity-related issues
- proposing HCloud create or modify commands

When relying on `hetzner-cloud`, inherit these rules from it:
- never expose tokens or credentials
- ask for confirmation before create or modify operations
- prefer showing the exact `hcloud` command before execution
- suggest snapshots before risky HCloud-side modifications

`syself` remains the source of truth for the SySelf Autopilot workflow and
support boundaries. `hetzner-cloud` is the source of truth for safe HCloud CLI
usage inside that workflow.

## Hard Scope Boundary
The skill must keep the distinction below explicit at all times.

SySelf Autopilot manages:
- The hosted management cluster.
- Cluster lifecycle through Kubernetes manifests.
- ClusterStack-driven tested releases.
- Installation of required software on bare metal machines.
- Adding and removing machines from workload clusters.
- Automated reconciliation, self-healing, and supported update paths.

The user or operator remains responsible for:
- Getting access to SySelf Autopilot and receiving the organization name.
- Obtaining the management-cluster kubeconfig from SySelf admins.
- Editing that kubeconfig so the namespace matches the assigned organization.
- Hetzner project setup, API credentials, SSH keys, and Robot access.
- Buying or exchanging bare metal servers.
- Confirming server compatibility and supported topology.
- Any infrastructure feature that SySelf support explicitly says is unsupported.

## Support-Verified Constraints
Treat the following as hard operational constraints for this skill.

1. UEFI-only bare metal servers that cannot be switched to Legacy BIOS mode are
   not usable for this SySelf provisioning flow. If the server is EFI-only and
   Hetzner cannot switch the boot mode, stop and tell the user the server must
   be exchanged.
2. Hetzner firewall and vSwitch are not supported in the reported SySelf support
   case. If the user relies on them for a failing bare metal bootstrap, warn
   that SySelf support identified this as incompatible and recommend reverting
   to a supported baseline before further debugging.
3. A cluster with only cloud control planes and bare metal workers may leave the
   hcloud CSI controller unschedulable. SySelf support recommended either:
   - ignore it if hcloud CSI is not needed, or
   - add at least one cloud worker node, or
   - knowingly schedule it on the control plane.
4. Do not promise support for OCI credential, MachineHealthCheck pause, or
   unsupported bootstrap tweaks unless the official docs explicitly cover them.

## Agent Behaviour Rules
1. Always identify whether the user is on SySelf Autopilot or on self-managed
   CAPH before executing any step.
2. Default to Autopilot. Only mention CAPH as context or contrast, not as the
   main execution path.
3. Before cluster work, verify management-cluster access and organization
   namespace setup.
4. Before bare metal onboarding, verify that the server is not UEFI-only and is
   not blocked by the Legacy BIOS limitation from the official troubleshooting
   page and support guidance.
5. Before using bare metal hosts, verify RAID handling and root device WWN.
6. Always prefer label-based bare metal host selection. Do not rely on random
   host selection in production.
7. Do not propose unsupported Hetzner firewall or vSwitch-based solutions as a
   standard supported setup.
8. Treat `kubectl` output, `Machine` state, `HetznerBareMetalHost` status, and
   `ClusterStackRelease` readiness as the authoritative runtime truth.
9. Surface support-boundary issues explicitly instead of papering over them.
10. If the user requests unsupported behavior, explain the boundary and propose
    the nearest supported alternative.

## Required Inputs
Before execution, collect or confirm all of the following.

### SySelf-side inputs
- Organization name from SySelf admins.
- Management-cluster kubeconfig from SySelf admins.
- User access is working with `kubelogin`.

### Hetzner-side inputs
- `HCLOUD_TOKEN`
- `HETZNER_ROBOT_USER`
- `HETZNER_ROBOT_PASSWORD`
- `SSH_KEY_NAME`
- `HETZNER_SSH_PUB_PATH`
- `HETZNER_SSH_PRIV_PATH`

### Cluster design inputs
- `CLUSTER_NAME`
- Target Kubernetes minor version supported by the current ClusterStack.
- Hetzner region, typically one region for control plane.
- HCloud control plane machine type.
- Whether the cluster needs cloud workers, bare metal workers, or both.
- If using bare metal workers: server IDs, intended labels, and root disk WWNs.

## Canonical Workflow

### Phase 0. Classify the mode
Goal: ensure the agent uses the managed Autopilot flow.

Checklist:
- Confirm the user intends to use SySelf Autopilot.
- If the user mentions `kind`, `clusterctl init`, bootstrap clusters, or pivoting,
  clarify that those belong to self-managed CAPH and are not the default path
  for this skill.

### Phase 1. Prepare local tooling
Required tools from official docs:
- `kubectl`
- `kubelogin`
- `helm`
- `hcloud` CLI when automating Hetzner preparation

Recommended verification:
```bash
kubectl version --client
kubectl oidc-login --help >/dev/null
helm version
hcloud version
```

### Phase 2. Configure management-cluster access
This is mandatory and must happen before any cluster operations.

1. Obtain the management kubeconfig from SySelf admins.
  There is also an official `kubeconfig.yaml` resource on the Autopilot access
  page, but it is gated behind login. If the user is authenticated in the docs
  portal, they may be able to copy or download it there. Do not assume a
  public direct URL exists.
2. Save it locally, for example as `management-kubeconfig.yaml`.
3. Update the namespace in that kubeconfig to the organization namespace given
   by SySelf. The docs explicitly require replacing it with your organization.
4. Restrict file permissions:
```bash
chmod 600 management-kubeconfig.yaml
```
5. Export it:
```bash
export KUBECONFIG="$PWD/management-kubeconfig.yaml"
```
6. Authenticate with SySelf Autopilot by running a simple command such as:
```bash
kubectl get clusters
```
This should open the browser for OIDC login if needed.

If no clusters exist yet, `No resources found` in the organization namespace is
not an error.

### Phase 3. Prepare Hetzner account and credentials
Follow the official Hetzner account preparation flow.

At this phase, the agent should also load and apply the `hetzner-cloud` skill
before issuing or recommending `hcloud` commands.

1. Create or select the HCloud project.
2. Generate a read-write HCloud API token.
3. Create an SSH key and upload the public key to HCloud.
4. Create the Hetzner Robot webservice user for bare metal operations.
5. Export the required environment variables.

Recommended environment variables:
```bash
export HCLOUD_TOKEN="<hcloud-token>"
export SSH_KEY_NAME="<ssh-key-name-in-hcloud-and-robot>"
export HETZNER_SSH_PUB_PATH="$HOME/.ssh/<key>.pub"
export HETZNER_SSH_PRIV_PATH="$HOME/.ssh/<key>"
export HETZNER_ROBOT_USER="<robot-user>"
export HETZNER_ROBOT_PASSWORD="<robot-password>"
export CLUSTER_NAME="mycluster"
export HCLOUD_REGION="nbg1"
export CONTROL_PLANE_MACHINE_TYPE_HCLOUD="cpx42"
```

### Phase 4. Create management-cluster secrets
Create the secrets in the SySelf Autopilot management cluster.

The official flow requires:
- `hetzner` secret for HCloud and Robot credentials.
- `robot-ssh` secret for bare metal provisioning via SSH.

Use the helper script:
- `scripts/02-create-management-secrets.sh`

### Phase 5. Preflight for bare metal supportability
Before onboarding bare metal workers, explicitly check the following.

1. Server is not blocked by the Legacy BIOS limitation.
2. RAID state is compatible. If the machine came with RAID enabled, follow the
   official disk wiping guide before registering the host.
3. Do not proceed with unsupported Hetzner firewall or vSwitch-based network
   assumptions for a failing bootstrap.
4. Ensure the SSH key name used in secrets matches the key present in Hetzner.

Stop conditions:
- EFI-only server with no Legacy BIOS option.
- User expects SySelf to support Hetzner firewall or vSwitch for the failing
  bootstrap path.

### Phase 6. Register bare metal hosts
Create a `HetznerBareMetalHost` per server in the management cluster.

Use the template:
- `templates/hetznerbaremetalhost.yaml`

Rules:
- Include `serverID`.
- Prefer explicit labels such as cluster scope and worker role.
- Include `rootDeviceHints.wwn` when known.
- If WWN is not known, apply without it first, inspect status, then patch it.

Recommended commands:
```bash
kubectl apply -f templates/hetznerbaremetalhost.yaml
kubectl get hetznerbaremetalhost
kubectl describe hetznerbaremetalhost <name>
```

If WWN is unknown:
```bash
kubectl get hbmh <name> -o yaml | yq .status.hardwareDetails.storage
```
or on the server itself:
```bash
lsblk -o name,WWN
```

Use the helper script:
- `scripts/04-register-baremetal-hosts.sh`

### Phase 7. Create ClusterStack release objects
Apply the official-style ClusterStack and HetznerClusterStackReleaseTemplate.

Use the template:
- `templates/clusterstack.yaml`

Notes:
- Standard official example includes `controlplaneamd64hcloud` and
  `workeramd64hcloud` node images.
- Bare metal workers are added through cluster topology and registered
  `HetznerBareMetalHost` resources, not through a separate bootstrap-cluster
  workflow in this skill.

Recommended verification:
```bash
kubectl apply -f templates/clusterstack.yaml
kubectl get clusterstack
kubectl get clusterstackreleases
kubectl get HetznerNodeImageReleases
```

Do not proceed until the intended `ClusterStackRelease` is ready.

### Phase 8. Create the workload cluster
Apply the cluster manifest through the management cluster.

Use the template:
- `templates/cluster.yaml`

For the main supported bare metal worker flow:
- control plane on HCloud
- workers on `workeramd64baremetal`
- host selection via labels using `workerHostSelectorBareMetal`

Recommended verification:
```bash
kubectl apply -f templates/cluster.yaml
kubectl get cluster
kubectl get machines
```

Use the helper script:
- `scripts/05-apply-cluster.sh`

### Phase 9. Get workload-cluster kubeconfig and verify access
The official docs include a workload kubeconfig retrieval step after cluster
creation. Use the documented command from the current Autopilot docs version
available to the user.

Then:
```bash
export KUBECONFIG="$PWD/<workload-kubeconfig-file>"
kubectl get nodes -o wide
kubectl get pods -A
```

Use the helper script:
- `scripts/06-verify-workload-access.sh`

### Phase 10. Day-2 cluster management

#### Add bare metal workers
- Register additional `HetznerBareMetalHost` resources.
- Add or scale `workeramd64baremetal` MachineDeployments.
- Prefer `workerHostSelectorBareMetal` with `matchLabels`.

#### Scale HCloud workers
- Edit `spec.topology.workers.machineDeployments[].replicas`.
- Use distinct MachineDeployments per machine type.

#### Make control plane HA
- Set `spec.topology.controlPlane.replicas` to an odd number.
- Prefer 3 or 5 depending on cluster size.

#### Remove specific nodes
- Annotate the Cluster API `Machine` object with:
```bash
kubectl annotate machine <machine-name> "cluster.x-k8s.io/delete-machine"=""
```
- Then reduce the corresponding replica count in the Cluster manifest.

#### Reboot bare metal nodes in-place
Only for controlled maintenance.

Management cluster:
```bash
kubectl annotate machine <machine-name> cluster.x-k8s.io/paused=true
```

Workload cluster:
```bash
kubectl drain <node-name> --ignore-daemonsets
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-name>
kubectl uncordon <node-name>
```

Management cluster after maintenance:
```bash
kubectl annotate machine <machine-name> cluster.x-k8s.io/paused-
```

#### Autoscaling
- Supported through Cluster Autoscaler in the workload cluster.
- A useful pattern is bare metal base capacity plus HCloud burst capacity.
- Use autoscaler annotations on MachineDeployments where needed.

#### Upgrades
- Follow the Autopilot update-cluster docs for the user’s current docs version.
- The agent must tell the user to switch docs version to the current cluster
  version before reading upgrade instructions.
- Do not invent upgrade steps not shown for the relevant version.

## Special Handling for Bare Metal Worker Clusters
When the cluster has cloud control planes and only bare metal workers:
- Watch for CSI controller pods stuck in `Pending`.
- This can happen because the CSI controller avoids root servers and the only
  remaining schedulable cloud node is tainted as control plane.
- Supported guidance from SySelf support is:
  - ignore hcloud CSI if not needed,
  - add at least one cloud worker node, or
  - knowingly allow scheduling onto the control plane.

Do not silently patch add-ons in a way that fights ClusterAddon reconciliation
unless the user explicitly wants a temporary workaround and understands it may be
overwritten.

## Troubleshooting Rules

### Bare metal registration or bootstrap failure
Check in this order:
1. Legacy BIOS requirement and UEFI-only incompatibility.
2. RAID or leftover disk state.
3. SSH key name mismatch.
4. Unsupported Hetzner firewall or vSwitch usage.
5. `HetznerBareMetalHost` status and hardware details.

### MachineHealthCheck loops
- Do not assume the fix is a custom MHC pause or unsupported annotation.
- First verify supported infrastructure baseline.
- If the cluster uses unsupported network features, recommend rollback to a
  supported baseline before further remediation.

### Stuck control plane provisioning on HCloud
- Regional HCloud capacity may block new control plane nodes.
- Bare metal control planes avoid this class of issue, but switching control
  plane class is a rolling replacement and must be planned.

## Artifacts in This Skill
- `templates/management-kubeconfig.yaml`:
  local template for the kubeconfig file received from SySelf admins.
- `templates/clusterstack.yaml`:
  official-style ClusterStack and HetznerClusterStackReleaseTemplate.
- `templates/cluster.yaml`:
  workload cluster manifest for HCloud control planes and bare metal workers.
- `templates/hetznerbaremetalhost.yaml`:
  one or more bare metal hosts with labels and WWN placeholders.
- `scripts/01-validate-access.sh`:
  validate tooling and management-cluster access.
- `scripts/03-prepare-management-kubeconfig.sh`:
  copy the kubeconfig received from SySelf admins and set the organization namespace.
- `scripts/02-create-management-secrets.sh`:
  create `hetzner` and `robot-ssh` secrets.
- `scripts/04-register-baremetal-hosts.sh`:
  apply host manifests and print follow-up checks.
- `scripts/05-apply-cluster.sh`:
  apply ClusterStack and Cluster manifests and print watch commands.
- `scripts/06-verify-workload-access.sh`:
  validate workload-cluster access after kubeconfig retrieval.

## Anti-Patterns
Never do these without explicit user override and risk acknowledgment.
- Do not create local kind bootstrap clusters for Autopilot.
- Do not run `clusterctl init` as part of the Autopilot flow.
- Do not recommend `clusterctl move` or pivoting for managed Autopilot.
- Do not present Hetzner firewall or vSwitch as supported SySelf baseline for
  failing bare metal bootstrap.
- Do not promise UEFI-only server compatibility.
- Do not use unlabeled bare metal host selection for production.
- Do not treat self-managed CAPH examples as production Autopilot instructions.

## Completion Criteria
The skill has completed its main job when all of the following are true:
- management kubeconfig exists and namespace matches the organization name
- Autopilot management-cluster access works
- Hetzner secrets exist in the management cluster
- `HetznerBareMetalHost` resources are applied and validated
- ClusterStack release is ready
- workload cluster manifest is applied
- workload cluster can be reached with kubeconfig
- agent can guide day-2 operations without leaving the supported SySelf scope