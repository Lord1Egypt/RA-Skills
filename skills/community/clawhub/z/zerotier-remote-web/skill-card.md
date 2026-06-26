## Description: <br>
Configures OpenClaw Gateway for ZeroTier-based remote web access, with scripts to check status, enable remote access, disable it, and return to local-only access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoyf0571](https://clawhub.ai/user/maoyf0571) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to make a local OpenClaw Control UI reachable from trusted devices on the same ZeroTier network without exposing a public IP address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open the OpenClaw admin gateway broadly and weaken authentication settings. <br>
Mitigation: Install only when remote administrative web access is intended; prefer binding to the ZeroTier IP or firewalling port 1880 to the ZeroTier network, and keep authentication protections enabled where possible. <br>
Risk: The skill exposes or depends on an OpenClaw gateway token for remote access. <br>
Mitigation: Do not share the token, restrict ZeroTier membership to trusted devices, and rotate the token if it may have been disclosed. <br>
Risk: Gateway configuration changes can disrupt local access. <br>
Mitigation: Use the generated OpenClaw configuration backup and the disable or restore workflow to return to local-only access if the gateway is disrupted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maoyf0571/zerotier-remote-web) <br>
- [ZeroTier](https://zerotier.com) <br>
- [ZeroTier documentation](https://zerotier.atlassian.net/wiki/) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit ~/.openclaw/openclaw.json, restart the OpenClaw Gateway, and print remote access URLs and token status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
