## Description: <br>
Production-ready security hardening for VPS running OpenClaw AI agents. Includes SSH hardening (custom port), firewall, audit logging, credential management, and intelligent alerting. Follows BSI IT-Grundschutz and NIST guidelines with minimal resource overhead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcusGraetsch](https://clawhub.ai/user/MarcusGraetsch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to harden dedicated Ubuntu or Debian VPS hosts running OpenClaw agents with SSH, firewall, audit logging, credential permission checks, and alerting controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes high-impact root SSH and firewall changes that can disrupt remote access. <br>
Mitigation: Install only on a disposable or dedicated VPS, keep an existing SSH session open, and verify the chosen SSH port is reachable before applying or relying on firewall changes. <br>
Risk: Security telemetry can be forwarded to external alert services when alerting is configured. <br>
Mitigation: Enable Telegram, Discord, Slack, email, or webhook reporting only when that third-party service is acceptable for the system's security logs. <br>
Risk: The evidence security verdict is suspicious because the skill changes root-level security controls. <br>
Mitigation: Review the installer and related scripts before deployment, test in a VM first, and follow the evidence guidance for dedicated VPS use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarcusGraetsch/vps-openclaw-security-hardening) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational hardening steps and verification guidance for a dedicated VPS.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
