## Description:

Create and manage HTTPS, SOCKS, or WireGuard proxies via the URnetwork API and MCP server for country, region, city, or provider-specific network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcolwell](https://clawhub.ai/user/xcolwell)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to authenticate to URnetwork, find available proxy locations, and create HTTPS, SOCKS, or WireGuard proxy configurations for selected countries, regions, cities, or egress providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to collect and reuse a URnetwork auth code or JWT, which can expose proxy account access if mishandled.

Mitigation: Treat auth codes and JWTs as credentials, avoid placing them in untrusted chats or logs, and prefer temporary or session-only storage.

Risk: WireGuard proxy configuration can route all device traffic through the proxy.

Mitigation: Review requests to enable WireGuard and require explicit user intent before creating or applying system-wide proxy configuration.

Risk: Proxy location and provider selection can affect traffic routing, policy compliance, and user expectations.

Mitigation: Confirm the requested country, region, city, or provider with the user and use the documented location type filters before creating proxy configurations.

## Reference(s):

- [URnetwork API specification](https://github.com/urnetwork/connect/blob/main/api/bringyour.yml)
- [URnetwork API endpoint](https://api.bringyour.com)
- [URnetwork MCP server](https://mcp.bringyour.com)
- [ClawHub skill page](https://clawhub.ai/xcolwell/skills/proxy-vpn)
- [ClawHub publisher profile](https://clawhub.ai/user/xcolwell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and proxy configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTPS proxy URLs, SOCKS proxy settings, WireGuard configuration text, location identifiers, provider identifiers, and credential handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
