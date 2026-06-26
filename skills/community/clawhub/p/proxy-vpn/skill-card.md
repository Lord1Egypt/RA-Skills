## Description: <br>
Create and manage HTTPS, SOCKS, or WireGuard proxies via the URnetwork API to connect through specific countries, regions, or cities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcolwell](https://clawhub.ai/user/xcolwell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to find URnetwork locations and create authenticated proxy configurations for web browsing, scraping, sockets, UDP, or system-wide routing. It helps choose between HTTPS, SOCKS, and WireGuard based on the user's requested connection target and protocol needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to handle auth codes and reusable bearer tokens for a URnetwork account. <br>
Mitigation: Treat auth codes and JWTs as secrets, avoid logging or storing them in plain text, and rotate them if exposed. <br>
Risk: The skill can create proxy sessions broadly, including loops over multiple egress IPs or providers. <br>
Mitigation: Require explicit user confirmation before creating proxies, especially bulk egress-IP or provider loops. <br>


## Reference(s): <br>
- [URnetwork API specification](https://github.com/urnetwork/connect/blob/main/api/bringyour.yml) <br>
- [URnetwork API endpoint](https://api.bringyour.com) <br>
- [URnetwork MCP endpoint](https://mcp.bringyour.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with curl examples and proxy configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTPS proxy URLs, SOCKS settings, or WireGuard configuration details returned by URnetwork.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
