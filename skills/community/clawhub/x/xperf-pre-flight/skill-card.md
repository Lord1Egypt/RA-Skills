## Description: <br>
Pre-flight check for GPU cluster nodes - node validation before training, check cluster node health, is my GPU node ready. 26 health checks covering GPU, PCIe, RDMA/IB, Docker, IOMMU, NUMA, firewall, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ops-xperf](https://clawhub.ai/user/ops-xperf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to run local readiness checks on bare-metal GPU cluster nodes before training, after provisioning, during periodic health monitoring, or while troubleshooting configuration drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that optional switch validation can run arbitrary shell commands when SWITCH_CLI_CMD is set. <br>
Mitigation: Review the shell scripts before installation, avoid setting SWITCH_CLI_CMD, and skip check 1.25 unless you control the exact switch command. <br>
Risk: Cross-node and switch checks can contact peer nodes or switch targets supplied by environment variables. <br>
Mitigation: Use only authorized peer and switch targets with least-privileged read-only credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ops-xperf/xperf-pre-flight) <br>
- [ClusterReady](https://clusterready.xperf.ai/) <br>
- [Xperf](https://xperf.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with bash commands; the invoked preflight script emits JSON to stdout and diagnostics to stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on Linux GPU cluster nodes and supports environment variables for selected checks, strict mode, peer IPs, mount points, and switch validation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
