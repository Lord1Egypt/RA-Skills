## Description: <br>
Audits and applies VPS security hardening for Ubuntu hosts, including firewall, fail2ban, SSH, and sysctl checks or changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to review an Ubuntu VPS security posture and, when intentionally executed, apply host hardening changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change firewall policy, restart fail2ban, and overwrite administrator security configuration by default. <br>
Mitigation: Run it first with --report or --dry-run, test on a non-production VPS, take backups, and confirm out-of-band access before applying changes. <br>
Risk: Existing fail2ban and sysctl configuration may be replaced during hardening. <br>
Mitigation: Review and preserve current configuration files before execution, then apply any hardening changes manually when rollback requirements are strict. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kingaiwork/vps-security-hardener) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON audit or hardening status with concise agent guidance as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can make host-level configuration changes when run without --report or --dry-run.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
