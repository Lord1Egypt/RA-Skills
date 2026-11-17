## Description:

Pre-flight check for GPU cluster nodes, covering node readiness before training across GPU, PCIe, RDMA/InfiniBand, Docker, IOMMU, NUMA, firewall, BIOS, and related health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ops-xperf](https://clawhub.ai/user/ops-xperf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cluster operators use this skill to check whether bare-metal GPU cluster nodes are ready before running workloads, after provisioning, during periodic monitoring, or while troubleshooting hardware and configuration drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags unsafe switch and container checks that require manual review before production installation.

Mitigation: Review the skill before installing it on production or privileged cluster nodes, and run checks with the least privilege that still permits the required diagnostics.

Risk: Switch validation can execute a direct switch command or connect to a switch over SSH.

Mitigation: Avoid SWITCH_CLI_CMD unless the environment is fully trusted, require normal SSH host-key verification for switches, and limit switch credentials to the access needed for validation.

Risk: Container-based GPU checks may pull or run runtime images during diagnostics.

Mitigation: Use pinned and approved container images before running the container checks in production environments.

Risk: Shared filesystem checks write a temporary marker file to the selected mount point.

Mitigation: Set MOUNT_POINT deliberately so the check targets an approved shared filesystem path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ops-xperf/skills/xperf-pre-flight)
- [ClusterReady](https://clusterready.xperf.ai/)
- [Xperf](https://xperf.ai/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; the preflight script emits JSON results to stdout and diagnostics to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports environment variables for node ID, selected checks, strict mode, peer IPs, shared mount point, and switch validation settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
