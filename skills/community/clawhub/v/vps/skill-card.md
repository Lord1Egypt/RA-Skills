## Description: <br>
Provision, secure, and manage virtual private servers with practical hosting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to plan, secure, and manage VPS hosting workflows, including initial setup, SSH hardening, firewalls, monitoring, backups, networking, and cost controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying VPS guidance directly to production infrastructure can change SSH access, firewall exposure, backups, reboots, or deletion behavior. <br>
Mitigation: Review proposed SSH, firewall, backup, reboot, and deletion steps before applying them to production servers. <br>
Risk: Incorrect ordering of access-hardening steps can lock administrators out of a server. <br>
Mitigation: Test SSH key access and provider console access before disabling password or root login, and allow the active SSH port before enabling firewall rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/vps) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with prose, checklists, and command-oriented recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only skill; no executable code or automatic server actions are bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
