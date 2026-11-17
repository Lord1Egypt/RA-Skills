## Description:

Detect SESSION-STATE.md changes from cron/background tasks and notify main session. Solves the 'cron writes, main session forgets' problem in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyzh09](https://clawhub.ai/user/tyzh09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to detect when background or cron tasks append updates to SESSION-STATE.md, then surface those updates to the main agent session before substantive responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background processes can write untrusted content into SESSION-STATE.md that the main agent may later read.

Mitigation: Treat imported session-state content as untrusted data and review which processes are allowed to write to SESSION-STATE.md.

Risk: The helper can truncate SESSION-STATE.md after reading when the file exceeds its line threshold.

Mitigation: Disable or gate auto-truncation unless backups, locking, and retention requirements are in place.

Risk: The optional nohup watcher can leave a background process running beyond the current session.

Mitigation: Use the watcher only when explicitly needed and manage it with a clear start/stop process.

Risk: The daemon stop command uses a broad process-name match.

Mitigation: Replace broad pkill stopping with PID-based control before operational use.

## Reference(s):

- [Optional Event-Driven Watch README](artifact/scripts/README-event-driven.md)
- [Session State Watch on ClawHub](https://clawhub.ai/tyzh09/skills/session-state-watch)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown documentation with bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a shell helper for mtime checks, optional inotify watch mode, and example Python code for appending session-state updates.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
