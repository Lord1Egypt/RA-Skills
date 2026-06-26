## Description: <br>
Helps agents temporarily use X-VPN MCP tools to route geo-sensitive requests through a specific region when a task hits geo-blocking or explicitly requires a regional view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xvpn-bot](https://clawhub.ai/user/xvpn-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when web or API work is blocked by geography or must be observed from a specific country. It guides the agent to connect through X-VPN MCP for the geo-sensitive step, then disconnect or restore the prior egress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or using the local X-VPN MCP server can change local VPN daemon configuration and route machine traffic through a selected VPN region. <br>
Mitigation: Install only if the publisher is trusted, inspect or verify the installer source before running it, and restore or disconnect the VPN egress after the geo-sensitive task is complete. <br>
Risk: Leaving a VPN tunnel connected after the required step can slow unrelated work, change region-dependent results, or consume free-tier connection budget. <br>
Mitigation: Record the starting VPN state with xvpn_get_overview and disconnect or restore the prior location before yielding back to the user. <br>
Risk: Free-tier connections may fail for non-free locations or drop during longer, data-heavy tasks. <br>
Mitigation: Use free-tier location discovery when applicable, surface upgrade or quota messages clearly, and ask the user before opening a new free connection or upgrading. <br>


## Reference(s): <br>
- [X-VPN MCP Skill](artifact/SKILL.md) <br>
- [Task integration](artifact/references/task-integration.md) <br>
- [Call patterns](artifact/references/call-patterns.md) <br>
- [Locations](artifact/references/locations.md) <br>
- [Error recovery](artifact/references/error-recovery.md) <br>
- [Free tier](artifact/references/free-tier.md) <br>
- [X-VPN MCP installer](https://app.xvpncdn.com/rpc788pbdq/install.sh) <br>
- [X-VPN account settings](https://xvpn.io/account/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline tool calls and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool call sequences for X-VPN connection, status, location discovery, cleanup, and recovery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
