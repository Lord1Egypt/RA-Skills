## Description:

金刚罩 is an OpenClaw system-guardian skill for safe gateway restarts, configuration checks, health patrols, resource cleanup, and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realhossie](https://clawhub.ai/user/realhossie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local OpenClaw installations by validating configuration changes, restarting the gateway with backup and rollback, running health checks, and cleaning aged sessions, backups, logs, and temporary files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups and audit logs may contain secrets from openclaw.json, .env, or configuration diffs.

Mitigation: Use environment-variable secrets where possible, restrict access to ~/.openclaw/backups and ~/.openclaw/data/system-guardian, and review config-audit.log for secret exposure.

Risk: Automated cleanup deletes old sessions, extra backups, logs, and matching temporary files.

Mitigation: Review the cleanup thresholds before scheduled runs and keep independent backups for data that must be retained.

Risk: Safe restart can restart OpenClaw Gateway and restore backed-up configuration files during rollback.

Mitigation: Run the config guard before configuration changes and execute the restart flow only when a gateway restart and possible rollback are acceptable.

Risk: The artifact README includes an unpinned git-clone installation path while server-resolved provenance is unavailable.

Mitigation: Install from the validated ClawHub release or verify the exact external repository commit before using the git-clone path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realhossie/skills/system-guardian)
- [Publisher profile](https://clawhub.ai/user/realhossie)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Bash commands and structured status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include health summaries, warnings, critical status lines, exit codes, and maintenance guidance.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, _meta.json, and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
