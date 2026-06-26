## Description: <br>
Manages VMware NSX networking resources such as segments, gateways, NAT rules, routes, IP pools, and health checks through CLI or MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Infrastructure, platform, and network engineers use this skill to inspect and manage VMware NSX-T or NSX 4.x networking. It supports network segment, gateway, NAT, static route, IP pool, health, and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change VMware NSX networking and may disrupt connectivity if used with broad privileges or insufficient review. <br>
Mitigation: Use least-privilege NSX accounts, keep write access out of routine monitoring setups, and review write plans before enabling agent access. <br>
Risk: TLS safety can be weakened when verify_ssl is disabled for non-lab environments. <br>
Mitigation: Set verify_ssl to true with a trusted CA for production and reserve TLS bypass only for controlled lab systems. <br>
Risk: Password obfuscation in .env files may be mistaken for encryption. <br>
Mitigation: Treat .env password obfuscation as convenience only, restrict file permissions, and manage credentials through approved secret-handling processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-nsx) <br>
- [VMware NSX GitHub repository](https://github.com/zw008/VMware-NSX) <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured CLI or MCP guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute NSX administration workflows depending on connected agent permissions and user approval.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
