## Description: <br>
Designs, implements, and operates encrypted restic backups for Linux home directories with systemd automation, retention policies, and restore validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moep90](https://clawhub.ai/user/Moep90) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and Linux users use this skill to set up and validate encrypted home-directory backups with restic, systemd timers, retention jobs, and restore checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The root-level setup script accepts repository and password-file values that can later be interpreted as shell input. <br>
Mitigation: Review or fix the bootstrap script before running it with sudo and --apply; use only trusted simple values without shell metacharacters or newlines and inspect /etc/restic-home.env before enabling timers. <br>
Risk: Backup automation and retention jobs can create false confidence if the repository, schedule, or restore path is not validated. <br>
Mitigation: Confirm the repository and retention policy, verify snapshot output, run restic check, and perform a restore test before relying on automated backups. <br>


## Reference(s): <br>
- [Restic Home Backup Ops Checklist](references/ops-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Moep90/restic-home-backup-safe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce restic commands, systemd unit guidance, validation steps, and operator runbook text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
