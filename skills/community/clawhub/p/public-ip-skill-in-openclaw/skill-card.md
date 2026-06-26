## Description: <br>
查询当前机器的公网 IP 地址。用于需要确定服务器或客户端在互联网上的公开标识时。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trollhe](https://clawhub.ai/user/trollhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query the current machine's public IP address for network diagnostics, egress verification, and IP allowlist or firewall configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public IP lookup providers, which can reveal the environment's public egress IP and lookup activity to third parties. <br>
Mitigation: Use it only where outbound calls to ipify, ifconfig.me, ipapi.co, and api.myip.com are acceptable; avoid restricted, corporate, or anonymity-sensitive networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trollhe/public-ip-skill-in-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/trollhe) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [JSON from the helper script, with concise text guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns public_ip and per-service lookup details when available; exits nonzero if all lookup services fail.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
