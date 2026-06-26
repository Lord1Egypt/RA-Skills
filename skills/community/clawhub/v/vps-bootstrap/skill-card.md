## Description: <br>
Bootstrap a fresh VPS from zero to a fully operational OpenClaw deployment, with backup/restore and post-recovery verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lolaopenclaw](https://clawhub.ai/user/lolaopenclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to bootstrap, recover, migrate, and verify an OpenClaw deployment on an Ubuntu or Debian VPS. It is intended for full-server setup and disaster recovery workflows that include package installation, service setup, security hardening, credential restore, and post-deployment checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bootstrap script makes system-level package, firewall, SSH, fail2ban, service, and persistence changes on the VPS. <br>
Mitigation: Review the scripts before execution, keep console or out-of-band access available, and run only on a host where full-server changes are intended. <br>
Risk: SSH hardening and firewall changes can lock out an operator if key-based login or access rules are not working. <br>
Mitigation: Confirm SSH key login and emergency access before running bootstrap, and verify firewall and SSH settings immediately after changes. <br>
Risk: The restore script can replace workspace files, local agent instructions, cron data, secrets, keyrings, and account configuration from a backup archive. <br>
Mitigation: Restore only from a trusted backup, inspect archive contents first, and run the verification script after restore before resuming normal operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lolaopenclaw/vps-bootstrap) <br>
- [Publisher profile](https://clawhub.ai/user/lolaopenclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash scripts and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces server setup, restore, and verification steps for an agent to execute or adapt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
