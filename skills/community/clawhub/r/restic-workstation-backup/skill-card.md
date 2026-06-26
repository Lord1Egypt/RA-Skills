## Description: <br>
Design, implement, and operate encrypted restic backups for Linux home directories with encryption, deduplication, automated scheduling, and restore testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kiris-z](https://clawhub.ai/user/Kiris-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, workstation operators, and infrastructure teams use this skill to plan, install, validate, and operate encrypted restic backups for Linux home directories. It supports system-level and user-level scheduling, restore drills, retention policy setup, logging, alerting, and operational runbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure ongoing backup, prune, check, and restore-audit jobs with broad access to a Linux home directory. <br>
Mitigation: Review plan output before using --apply, use only repositories and alert email addresses under the operator's control, and confirm timers and retention policy before enabling scheduled jobs. <br>
Risk: Backup credentials and restored files may expose sensitive home-directory data if mishandled. <br>
Mitigation: Keep generated restic passwords in a separate secrets vault, preserve 0600 permissions on credential files, and avoid printing secrets in chat, logs, or scripts. <br>
Risk: Retention and prune operations can remove backup snapshots when run live. <br>
Mitigation: Review dry-run prune output and require explicit user confirmation before deleting snapshots or repository data. <br>


## Reference(s): <br>
- [Operator Runbook](references/runbook.md) <br>
- [Ops Checklist](references/ops-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Kiris-z/restic-workstation-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated shell/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plan-only output is available before apply mode; operational output can include installed scripts, systemd units, logs, validation evidence, and corrective guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
