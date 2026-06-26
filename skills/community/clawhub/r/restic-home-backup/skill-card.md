## Description: <br>
Designs, implements, and operates encrypted restic backups for Linux home directories with systemd automation, retention policies, and restore validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moep90](https://clawhub.ai/user/Moep90) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and home lab administrators use this skill to plan and apply encrypted restic backups for Linux home directories, including systemd timers, retention policies, and restore validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can make root-level changes and server security evidence reports that malformed repository or path inputs may lead to privileged command execution or unsafe file writes. <br>
Mitigation: Run the script in plan-only mode first, inspect generated values and /etc/restic-home.env, use trusted values for --repo, --password-file, --user, and --timezone, and require explicit --apply before enabling services or timers. <br>
Risk: Retention pruning or repository deletion can remove backup snapshots if run with the wrong repository or retention settings. <br>
Mitigation: Use a dedicated restic repository, confirm retention policy and repository endpoint before enabling prune timers, and require explicit confirmation before destructive restic operations. <br>


## Reference(s): <br>
- [Restic Home Backup Ops Checklist](references/ops-checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/Moep90/restic-home-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup setup guidance, generated scripts, systemd unit details, validation steps, and an operator runbook.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
