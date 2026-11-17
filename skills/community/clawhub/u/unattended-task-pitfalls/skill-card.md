## Description:

Hardening playbook for AI agent unattended and scheduled tasks, covering background execution, artifact verification, isolated-session context gaps, notifications, and self-healing retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mowenqwq](https://clawhub.ai/user/mowenqwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this Chinese-language playbook to design or debug cron jobs, scheduled backups, auto-reports, and other unattended agent tasks. It helps agents propose bounded execution, artifact checks, clearer notifications, and safer retry behavior for automation that may run without an active user session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background jobs and scheduled tasks can run longer than intended or become hard to audit.

Mitigation: Keep jobs bounded, write clear logs, and poll process state and artifacts before retrying or reporting success.

Risk: Examples involving scans, uploads, deletes, publishes, or state updates can cause damage if adapted too broadly.

Mitigation: Scope file operations to known workspaces, require explicit user approval for destructive actions, and add idempotency checks before retries.

Risk: Unattended automation may report success even when artifacts are corrupt or context is incomplete.

Mitigation: Verify artifacts before upload or state updates, preserve failure evidence, and cross-check scheduled-task conclusions against filesystem activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mowenqwq/skills/unattended-task-pitfalls)
- [Archive verification reference script](scripts/verify_archive.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell snippets and Python reference code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reusable archive-verification template and operational checklist guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill changelog, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
