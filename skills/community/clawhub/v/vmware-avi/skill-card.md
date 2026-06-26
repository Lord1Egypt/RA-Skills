## Description: <br>
AVI (NSX Advanced Load Balancer) application delivery and AKO Kubernetes operations for virtual services, pool members, SSL certificates, analytics, service engines, ingress diagnostics, sync diagnostics, and multi-cluster AKO status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect, troubleshoot, and manage VMware AVI/NSX ALB load balancing and AKO Kubernetes ingress environments. It supports read-only diagnostics plus approval-gated operational changes such as disabling virtual services, draining pool members, restarting AKO, applying AKO Helm upgrades, and forcing sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive VMware AVI controller credentials and Kubernetes kubeconfig data. <br>
Mitigation: Treat controller passwords and kubeconfig access as sensitive; prefer a secret manager over .env storage and restrict file permissions. <br>
Risk: Operational commands can affect live application delivery, including virtual service disablement, pool member drain, AKO restart, Helm upgrade, and forced sync. <br>
Mitigation: Require explicit human approval before write operations and review the planned impact before applying changes. <br>
Risk: Disabling TLS verification can hide controller identity or transport-security problems. <br>
Mitigation: Keep TLS verification enabled in production and use verify_ssl=false only for controlled lab environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-avi) <br>
- [Project homepage](https://github.com/zw008/VMware-AVI) <br>
- [VMware AVI Capabilities](references/capabilities.md) <br>
- [VMware AVI CLI Reference](references/cli-reference.md) <br>
- [VMware AVI Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration snippets, and MCP tool-use recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only diagnostics, approval-gated write commands, and operational checklists.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
