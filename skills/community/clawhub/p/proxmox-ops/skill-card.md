## Description: <br>
Ops-focused Proxmox VE management via REST API for monitoring, controlling, provisioning, and troubleshooting VMs and LXC containers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and infrastructure administrators use this skill to manage Proxmox VE environments through REST API patterns, helper shell commands, and operational guidance for VMs, LXC containers, storage, backups, and provisioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports powerful Proxmox operations that can stop, reboot, resize, roll back, delete, or provision VMs and containers. <br>
Mitigation: Manually verify VMID, node, backups, and intent before high-impact actions, and require explicit confirmation for destructive or difficult-to-reverse operations. <br>
Risk: Proxmox API tokens and ~/.proxmox-credentials can grant infrastructure access if exposed. <br>
Mitigation: Use least-privilege API tokens, keep credential files mode 600, avoid exposing secrets in responses, and rotate tokens immediately if they are disclosed. <br>
Risk: The helper examples use curl with TLS verification disabled for self-signed Proxmox certificates. <br>
Mitigation: Prefer trusted TLS certificates, remove the insecure curl flag where possible, and restrict agent network access to intended Proxmox hosts. <br>


## Reference(s): <br>
- [Proxmox Ops homepage](https://github.com/eddygk/proxmox-ops-skill) <br>
- [Proxmox Provisioning Reference](references/provisioning.md) <br>
- [Proxmox VE API Tokens](https://pve.proxmox.com/wiki/User_Management#pveum_tokens) <br>
- [Proxmox VE Certificate Management](https://pve.proxmox.com/wiki/Certificate_Management) <br>
- [ClawHub skill page](https://clawhub.ai/eddygk/proxmox-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and Proxmox REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Proxmox API endpoints, jq filters, credential setup guidance, and confirmation steps for high-impact operations.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
