## Description: <br>
Harden an OpenClaw Linux server with SSH key-only auth, UFW firewall, fail2ban brute-force protection, and credential permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to harden OpenClaw Linux servers during setup, security audits, or incident follow-up by applying SSH, firewall, fail2ban, credential permission, and gateway service checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH and firewall changes could lock an operator out of a remote server if key-based SSH or required ports are not already confirmed. <br>
Mitigation: Confirm key-based SSH in a separate session, allow all required firewall ports before enabling UFW, and keep console or out-of-band access available. <br>
Risk: The OpenClaw gateway service is configured as a persistent root service that restarts automatically. <br>
Mitigation: Install it only when persistent root operation is intended, and harden the service with least-privilege settings before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ppiankov/server-host-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands modify SSH, firewall, fail2ban, file permissions, and a systemd service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
