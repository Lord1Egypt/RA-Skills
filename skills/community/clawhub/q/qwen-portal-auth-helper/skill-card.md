## Description:

Automate qwen-portal OAuth authentication - solves the interactive TTY problem with tmux, provides monitoring and recovery tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jazzqi](https://clawhub.ai/user/jazzqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to recover qwen-portal authentication in OpenClaw automation, monitor qwen-backed cron tasks, and reset task state after successful re-authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent cron monitoring jobs.

Mitigation: Use setup-monitoring only after explicit user confirmation and document the exact crontab entry so it can be reviewed or removed.

Risk: OAuth links, device codes, and authentication reports may be written to shared temporary files or logs.

Mitigation: Treat generated logs and reports as sensitive, restrict access to shared systems, and delete temporary OAuth artifacts after recovery.

Risk: Reset commands modify OpenClaw scheduler state for a supplied task ID.

Mitigation: Run reset-task only with task IDs verified from trusted OpenClaw output and confirm the target task before writing scheduler state.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jazzqi/skills/qwen-portal-auth-helper)
- [Publisher profile](https://clawhub.ai/user/jazzqi)
- [README](artifact/README.md)
- [Quick recovery guide](artifact/examples/quick-recovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, terminal output, JSON command results, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local log and report files under /tmp and may update OpenClaw cron state when reset commands are used.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
