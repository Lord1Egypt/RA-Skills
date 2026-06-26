## Description: <br>
Real-time security monitoring dashboard for OpenClaw and Linux server infrastructure. Monitors gateway status, network security, public exposure, system updates, SSH access, TLS certificates, and resource usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vegasbrianc](https://clawhub.ai/user/vegasbrianc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to install and run a localhost security dashboard for OpenClaw and Linux server monitoring, including gateway status, network exposure, SSH access, TLS, updates, and resource checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent boot-starting dashboard service. <br>
Mitigation: Install only on servers where a persistent localhost monitoring service is expected, and review the generated systemd service before enabling it. <br>
Risk: The service account may receive passwordless sudo rights for host inspection commands. <br>
Mitigation: Prefer the dedicated service user, avoid root mode, and review /etc/sudoers.d/openclaw-dashboard before deployment. <br>
Risk: The unauthenticated local API exposes detailed host security information. <br>
Mitigation: Keep the service bound to 127.0.0.1 or a trusted tunnel, and treat API output as sensitive security data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vegasbrianc/security-dashboard) <br>
- [Skill documentation](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Configuration] <br>
**Output Format:** [Web dashboard, JSON API responses, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security metrics and alerts are generated from local host inspection and should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
