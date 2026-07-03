## Description: <br>
This skill helps agents manage VMware NSX networking, including segments, gateways, NAT, routing, IP pools, fabric inventory, health checks, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to inspect, operate, and troubleshoot VMware NSX networking through CLI and MCP workflows. It covers NSX segments, Tier-0 and Tier-1 gateways, NAT, static routes, IP pools, fabric inventory, health status, and connectivity troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live VMware NSX network infrastructure. <br>
Mitigation: Review carefully before production use, prefer dry-run CLI workflows for changes, and confirm whether MCP write tools require explicit approval in the connected agent. <br>
Risk: Over-privileged credentials could amplify the impact of incorrect or unauthorized network changes. <br>
Mitigation: Use a least-privilege NSX service account appropriate to the intended read or write operations. <br>
Risk: Insecure TLS or credential handling could expose NSX administrative access. <br>
Mitigation: Set verify_ssl to true with a trusted CA and avoid storing real admin passwords in plaintext .env files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-nsx) <br>
- [Source Homepage](https://github.com/zw008/VMware-NSX) <br>
- [Capabilities Reference](artifact/references/capabilities.md) <br>
- [CLI Reference](artifact/references/cli-reference.md) <br>
- [Setup Guide](artifact/references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include NSX Policy API operation plans, read-only checks, and write-operation guidance.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
