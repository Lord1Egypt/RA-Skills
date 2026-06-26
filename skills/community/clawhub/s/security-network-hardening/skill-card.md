## Description: <br>
Audit and harden an OpenClaw host and its network exposure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit Linux hosts running OpenClaw, review network exposure, and prepare approved firewall, permission, and OpenClaw gateway hardening changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firewall or network changes can interrupt current management access. <br>
Mitigation: Confirm the active management path, allowed source IPs or subnets, backups, and rollback steps before approving state-changing actions. <br>
Risk: Privileged firewall, permission, OpenClaw configuration, or commit changes may alter host behavior. <br>
Mitigation: Start with read-only audits, require explicit approval before fixes, and verify with OpenClaw audit, gateway status, UFW status, and listening-port checks after changes. <br>
Risk: Generated remediation guidance can be incorrect if host-specific ports or trusted sources are assumed. <br>
Mitigation: Use exact findings from the target host and confirm required ports, metrics scrapers, LAN ranges, and remote-access needs before applying rules. <br>


## Reference(s): <br>
- [OpenClaw Fix Patterns](references/openclaw-fix-patterns.md) <br>
- [UFW Playbook](references/ufw-playbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jimpang8/security-network-hardening) <br>
- [Publisher Profile](https://clawhub.ai/user/jimpang8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate firewall rule documentation and apply, rollback, or verification shell scripts when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
