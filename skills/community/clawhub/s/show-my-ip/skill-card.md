## Description: <br>
Show the current public IP address of the server. Use when asked about IP, public IP, or network identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check the public IPv4 and IPv6 address of the machine running the agent for network debugging, VPN or proxy checks, allowlisting, and server identity confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts ifconfig.me and exposes the host's public IP address to that service. <br>
Mitigation: Install and run it only in environments where sharing the host's public IP with ifconfig.me is acceptable. <br>


## Reference(s): <br>
- [ifconfig.me](https://ifconfig.me) <br>
- [ClawHub Skill Page](https://clawhub.ai/ericsantos/show-my-ip) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns IPv4 when available and may include IPv6.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
