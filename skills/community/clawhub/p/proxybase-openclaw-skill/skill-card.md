## Description: <br>
Purchase and manage SOCKS5 residential proxies via the ProxyBase API with cryptocurrency payments, including order creation, payment polling, proxy delivery, bandwidth monitoring, IP rotation, and top-ups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[proxybase-user](https://clawhub.ai/user/proxybase-user) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to buy, monitor, and configure paid ProxyBase residential SOCKS5 proxies for agent traffic, with human approval for cryptocurrency payment and optional gateway proxy injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently route OpenClaw gateway and exec traffic through a third-party proxy. <br>
Mitigation: Prefer per-command proxy use or manually sourced environment files unless global routing is intended; run inject-gateway with --dry-run first and keep the service backup for restoration. <br>
Risk: The skill stores API keys and proxy credentials locally. <br>
Mitigation: Keep generated state files private, avoid exposing API keys or proxy passwords in chat, and rotate or remove credentials when no longer needed. <br>
Risk: The skill can create a third-party account and handle paid cryptocurrency proxy orders. <br>
Mitigation: Install only when ProxyBase is trusted, review package and currency choices before payment, and require explicit human approval before sending funds. <br>


## Reference(s): <br>
- [ProxyBase Homepage](https://proxybase.xyz) <br>
- [ProxyBase API](https://api.proxybase.xyz/v1) <br>
- [ProxyBase ClawHub Page](https://clawhub.ai/proxybase-user/proxybase-openclaw-skill) <br>
- [OpenClaw Configuration Reference](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON snippets, and generated shell configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state files for credentials, order tracking, and proxy environment variables.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
